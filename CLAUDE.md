# Low Value Content: guide for Claude sessions

Satirical editorial T-shirt brand of Nelson Grey LLC, pre-launch. This repo holds the business plan, the 100-concept catalog, shirt designs, and the static website. Read `README.md` first, then `docs/product/concept-catalog.md` for product status.

## Commands
- `python3 scripts/check-site.py`: validates every HTML page (lang, title, viewport, description, local links) and the Firebase JSON config. CI runs the same.
- `firebase emulators:start --only hosting`: preview `website/dist/` locally (localhost is never gated).
- `python tools/business-plan/build_business_plan.py`: regenerates the business plan `.docx` (needs `python-docx`). Not part of the site or deploy.
- `gitleaks detect --source . --config .gitleaks.toml --redact`: secret scan.

## Layout
- `website/dist/`: the deployed static site (plain HTML, CSS, vanilla JS; **no framework and no build step**, by decision).
- `website/coming-soon/`: standalone production placeholder. `main` deploys this instead of `dist/` unless the `SHOW_COMING_SOON` variable in the `production` GitHub Environment is exactly `false`.
- `firebase.{dev,staging,prod}.json`: per-environment hosting config; the deploy workflow copies the right one to `firebase.json`. Dev and staging send noindex and a strict CSP.
- `docs/`, `design/`, `tools/`: business plan, concept catalog, shirt art and mockups, generator script.
- `sources/`: read-only mirror of the original ChatGPT project. Never edit, rename, move, or delete anything in it.

## Rules that must keep holding
- Flow is `feature/*` → `develop` → `staging` → `main`. Never push or open a PR to `main`, and never deploy to prod, unless the user explicitly says to. Prod is **not live**: it shows the coming-soon page.
- Slogans and the brand name are not trademark-cleared. Never present them as cleared in copy or listings.
- Dev and staging sit behind a Google sign-in gate (`website/dist/assets/auth-gate.js`). The allowlist comes from the `ALLOWED_EMAIL_DOMAINS` and `ALLOWED_EMAILS` secrets in each GitHub Environment and is written to `assets/env-config.js` at deploy time. An empty allowlist locks everyone out. Never commit real addresses or API keys.
- Deploys are keyless (Workload Identity Federation) because org policy forbids service-account keys. Never create or commit a service-account key.
- The org is on the GitHub Free plan: private repos have no branch protection, secret scanning, or code scanning. CI's "Promotion guard" is advisory only.

## Working style with this user (Mark Nelson)
- Give a recommendation and continue; outward-facing or costly actions (publishing, pushing to `main`, deploying to prod, creating cloud resources, spending money) need their explicit say-so.
- Commit in small commits ending with the co-author line from the session, and open PRs against `develop`.
- Be explicit about what is verified versus not (for example, real Google sign-in has only been tested up to the popup).
