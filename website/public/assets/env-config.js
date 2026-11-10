// Replaced at deploy time by .github/workflows/deploy-website.yml for dev and staging.
// Empty allowlist = nobody gets past the non-prod gate (fails closed). Production is never gated.
window.__ENV_GATE__ = { domains: [], emails: [], apiKey: '', appId: '' };
