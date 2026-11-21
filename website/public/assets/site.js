// Mobile navigation toggle. Kept as an external file so the dev and staging
// Content-Security-Policy (script-src 'self') does not block it.
const button = document.querySelector('.menu-button');
const nav = document.querySelector('#site-navigation');
button?.addEventListener('click', () => {
  const open = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', String(!open));
  nav?.classList.toggle('open', !open);
});
