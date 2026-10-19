// Non-prod access gate (same model as EnvironmentGate in vehicle-vitals):
// Google sign-in, allowed if the email's domain is in `domains` or the exact
// address is in `emails`. Empty allowlist denies everyone. Prod and localhost are never gated.
// Not a hard auth boundary: the allowlist ships in env-config.js, it only keeps the public out.
(function () {
  const host = window.location.hostname;
  const environment = /-staging\./.test(host) ? 'staging' : /-dev\./.test(host) ? 'development' : '';
  const isLocal = /^(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])$/.test(host);
  const root = document.documentElement;

  if (!environment || isLocal) { root.classList.add('auth-granted'); return; }
  root.classList.add('auth-required');

  const config = window.__ENV_GATE__ || {};
  const clean = list => (Array.isArray(list) ? list : []).map(v => String(v).trim().toLowerCase()).filter(Boolean);
  const domains = clean(config.domains);
  const emails = clean(config.emails);
  const projectId = 'low-value-content-' + (environment === 'staging' ? 'staging' : 'dev');
  const firebaseConfig = { projectId, apiKey: config.apiKey, appId: config.appId, authDomain: projectId + '.firebaseapp.com' };

  function isAuthorized(email) {
    email = (email || '').toLowerCase();
    if (!email || (!domains.length && !emails.length)) return false;
    return emails.includes(email) || domains.includes(email.split('@')[1]);
  }

  const style = document.createElement('link');
  style.rel = 'stylesheet';
  style.href = '/assets/auth-gate.css';
  document.head.appendChild(style);

  const SESSION_KEY = 'lvc_env_gate_email';
  const gate = document.createElement('div');
  gate.id = 'auth-gate';
  gate.innerHTML = '<section class="auth-gate-card" aria-labelledby="auth-gate-title"><img src="/assets/iconmark-11-content-cocktail.svg" alt=""><p class="auth-gate-label"></p><h1 id="auth-gate-title">Team access only.</h1><p>Sign in with an authorized Google account to view this website.</p><button class="auth-gate-button" type="button">Sign in with Google</button><p class="auth-gate-error" role="alert" aria-live="polite"></p></section>';
  gate.querySelector('.auth-gate-label').textContent = 'Restricted ' + environment + ' environment';
  const button = gate.querySelector('.auth-gate-button');
  const error = gate.querySelector('.auth-gate-error');

  function mount() { document.body.prepend(gate); }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);

  function grant(email) {
    root.classList.add('auth-granted');
    gate.remove();
    const revoke = document.createElement('button');
    revoke.className = 'auth-revoke';
    revoke.type = 'button';
    revoke.textContent = 'Sign out · ' + email;
    revoke.addEventListener('click', () => {
      try { sessionStorage.removeItem(SESSION_KEY); } catch (e) { /* ignore */ }
      window.location.reload();
    });
    document.body.appendChild(revoke);
  }

  let remembered = '';
  try { remembered = sessionStorage.getItem(SESSION_KEY) || ''; } catch (e) { /* ignore */ }
  if (isAuthorized(remembered)) {
    if (document.body) grant(remembered); else document.addEventListener('DOMContentLoaded', () => grant(remembered));
    return;
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  async function start() {
    if (!firebaseConfig.apiKey || !firebaseConfig.appId) {
      error.textContent = 'Sign-in is not configured for this environment.';
      button.disabled = true;
      return;
    }
    try {
      await loadScript('https://www.gstatic.com/firebasejs/12.19.0/firebase-app-compat.js');
      await loadScript('https://www.gstatic.com/firebasejs/12.19.0/firebase-auth-compat.js');
    } catch (e) {
      error.textContent = 'The sign-in service could not be loaded. Please refresh and try again.';
      button.disabled = true;
      return;
    }
    // Isolated Firebase app instance; nothing else on the site observes it.
    const app = window.firebase.initializeApp(firebaseConfig, 'lvc-environment-gate');
    const auth = app.auth();
    await auth.setPersistence(window.firebase.auth.Auth.Persistence.NONE);

    button.addEventListener('click', async () => {
      button.disabled = true;
      error.textContent = '';
      try {
        const provider = new window.firebase.auth.GoogleAuthProvider();
        provider.setCustomParameters({ prompt: 'select_account' });
        const result = await auth.signInWithPopup(provider);
        const email = result.user && result.user.email;
        if (isAuthorized(email)) {
          try { sessionStorage.setItem(SESSION_KEY, email.toLowerCase()); } catch (e) { /* ignore */ }
          grant(email.toLowerCase());
        } else {
          error.textContent = 'Your email (' + email + ') is not authorized to access this environment.';
        }
        await auth.signOut().catch(() => {});
      } catch (cause) {
        if (!cause || cause.code !== 'auth/popup-closed-by-user') {
          error.textContent = (cause && cause.message) || 'Sign-in failed. Please try again.';
        }
      } finally {
        button.disabled = false;
      }
    });
  }
  start();
})();
