# Low Value Content

[![CI](https://github.com/NelsonGrey/low-value-content/actions/workflows/ci.yml/badge.svg)](https://github.com/NelsonGrey/low-value-content/actions/workflows/ci.yml)
[![Deploy Website](https://github.com/NelsonGrey/low-value-content/actions/workflows/deploy-website.yml/badge.svg)](https://github.com/NelsonGrey/low-value-content/actions/workflows/deploy-website.yml)
![License: Proprietary](https://img.shields.io/badge/license-proprietary-lightgrey)

**Low Value Content** is an editorial apparel imprint of **Nelson Grey LLC**. Its garments record social media theater, algorithm anxiety, the creator economy, and other conditions of sustained online life.

This repository holds the whole project: the business plan, the product concept catalog, shirt design prototypes, launch mockups, and the website.

> **Status:** early development. The website is a placeholder landing page, and none of the names or slogans are trademark-cleared yet. See the [concept catalog](docs/product/concept-catalog.md) and the business plan.

| Environment | Branch | Firebase project | URL |
| --- | --- | --- | --- |
| Development | `develop` | `low-value-content-dev` | https://low-value-content-dev.web.app |
| Staging | `staging` | `low-value-content-staging` | https://low-value-content-staging.web.app |
| Production | `main` | `low-value-content-prod` | https://low-value-content-prod.web.app |

## Contents

- [The concept](#the-concept)
- [Repository layout](#repository-layout)
- [Getting started](#getting-started)
- [Website](#website)
- [Deployment](#deployment)
- [Non-prod access gate](#non-prod-access-gate)
- [Branching and releases](#branching-and-releases)
- [Business plan](#business-plan)
- [Documentation](#documentation)
- [Quality and security](#quality-and-security)
- [Contributing, security, and support](#contributing-security-and-support)
- [License](#license)

## The concept

The [concept catalog](docs/product/concept-catalog.md) organizes 100 shirt sayings into ten collections. Each entry is scored **Launch**, **Develop**, or **Hold**.

| # | Collection |
| --- | --- |
| 1 | Social Media Theater |
| 2 | Algorithm Anxiety |
| 3 | Creator Economy |
| 4 | Chronically Online |
| 5 | Artificial Authenticity |
| 6 | Future of Work |
| 7 | Productivity Theater |
| 8 | Performative Sustainability |
| 9 | Terms and Conditions |
| 10 | Optimized Human |

Six prototypes are in [design/prototypes/](design/prototypes/) and launch mockups are in [design/mockups/](design/mockups/).

## Repository layout

```
low-value-content/
├── docs/
│   ├── business-plan/      Business plan (.docx) and its QA renders (qa/draft, qa/final)
│   └── product/            Concept catalog, apparel manifest, and product notes
├── design/
│   ├── prototypes/         Shirt design SVGs and PNG previews
│   └── mockups/            Launch mockup images
├── tools/
│   └── business-plan/      build_business_plan.py (regenerates the .docx)
├── website/
│   ├── src/ public/        Astro storefront source and static assets
│   ├── coming-soon/        Standalone production placeholder
│   └── dist/               Build output served by Firebase Hosting (not committed)
├── sources/                Synced from the ChatGPT project. Read-only, do not edit.
├── .github/                Workflows, issue and PR templates, CODEOWNERS, Dependabot
├── .firebaserc             Firebase project aliases (dev / staging / prod)
└── firebase.json           Firebase Hosting configuration
```

## Getting started

Prerequisites:

- [Node.js](https://nodejs.org/) 18+ and the [Firebase CLI](https://firebase.google.com/docs/cli): `npm install -g firebase-tools`
- Python 3.11+ with `python-docx` (only to regenerate the business plan)
- Access to the three Firebase projects (to deploy by hand)

```bash
git clone https://github.com/NelsonGrey/low-value-content.git
cd low-value-content
git switch develop
firebase login
```

## Website

The website is one Astro project in [`website/`](website/). `npm run build` writes the static site to `website/dist/` (not committed), which Firebase Hosting serves, routing `/api/**` to the commerce function.

The **Royal House of Engagement** is the governing institution within the Low Value Content world. Low Value Content remains the portal, purveyor, owned domain, merchant, and garment maker's mark. Astro generates the homepage, ten product pages, the Realm, the Lineage, and the Royal Calendar from the master apparel manifest.

```bash
npm install --prefix website
npm run dev --prefix website
npm run build --prefix website
```

The Valebasse build uses Node.js 24 or newer. The existing commerce functions retain their own runtime configuration.

Preview locally:

```bash
npm run build --prefix website
firebase emulators:start --only hosting
```

## Deployment

Aliases are defined in [.firebaserc](.firebaserc):

```bash
firebase deploy --only hosting --project development   # low-value-content-dev
firebase deploy --only hosting --project staging       # low-value-content-staging
firebase deploy --only hosting --project production    # low-value-content-prod
```

### Automatic deploys

[.github/workflows/deploy-website.yml](.github/workflows/deploy-website.yml) builds and deploys the Astro storefront on every push to `develop`, `staging`, or `main` that changes `website/**`, the apparel manifest, Firebase configuration, or the workflow itself. Each branch maps to its own GitHub Environment (`development`, `staging`, `production`).

Deploys are keyless. The workflow authenticates with [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) because the organization policy `iam.disableServiceAccountKeyCreation` forbids service-account keys. Each Firebase project has a `github-deploy` service account (Firebase Hosting Admin only) and a GitHub OIDC provider that trusts only this repository and only that environment's branch (`develop`, `staging`, or `main`). Each GitHub Environment holds a `WIF_PROVIDER` variable with the provider's resource name. No credentials are stored in GitHub.

## Non-prod access gate

The dev and staging sites sit behind a Google sign-in wall (`website/public/assets/auth-gate.js`), the same model as `EnvironmentGate` in vehicle-vitals, modulo-squares, and sprout. Production and `localhost` are never gated. It keeps the public out; it is not a hard auth boundary, because the allowlist ships in the page.

A visitor gets in if their email's **domain** is in `ALLOWED_EMAIL_DOMAINS`, or their exact address is in `ALLOWED_EMAILS`. An empty allowlist locks everyone out. Both are comma-separated secrets set per GitHub Environment (`development`, `staging`); the deploy workflow writes them into `assets/env-config.js` at deploy time and fails if both are empty. The same workflow step passes the public Firebase web config from the `FIREBASE_WEB_API_KEY` and `FIREBASE_WEB_APP_ID` secrets.

**Grant someone access:** add their address to `ALLOWED_EMAILS` (or their domain to `ALLOWED_EMAIL_DOMAINS`) under *Settings → Environments → development / staging → Environment secrets*, then re-run the deploy for that branch.

**One-time setup per Firebase project** (`low-value-content-dev`, `low-value-content-staging`): register a Web app, enable **Google** under Authentication → Sign-in method, and add `<project>.web.app` under Authentication → Settings → Authorized domains.

Both environments also send `X-Robots-Tag: noindex, nofollow, noarchive` and a strict CSP (see `firebase.dev.json`, `firebase.staging.json`).

### Production coming-soon page

Until launch, production (`main`) serves a standalone coming-soon page from [website/coming-soon/](website/coming-soon/) instead of the full site. The deploy workflow swaps it in for `main` pushes. Dev and staging always deploy the full site. The page is `noindex` and collects no data.

The switch is the `SHOW_COMING_SOON` variable in the `production` GitHub Environment. It is `true` now, and anything other than the exact value `false` keeps the coming-soon page up (fails safe). **To go live:** set `SHOW_COMING_SOON` to `false` under *Settings → Environments → production → Environment variables*, then re-run the Deploy Website workflow on `main`.

## Branching and releases

```
feature/*  →  develop  →  staging  →  main
               (dev)      (staging)   (production)
```

`develop` is the default branch. Do not commit directly to `staging` or `main`; promote with pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md).

## Business plan

The plan is generated from code so it can be revised and rebuilt:

```bash
pip install python-docx
python tools/business-plan/build_business_plan.py
```

The output is [docs/business-plan/Low_Value_Content_Business_Plan.docx](docs/business-plan/Low_Value_Content_Business_Plan.docx). Page renders used for visual QA are in [docs/business-plan/qa/](docs/business-plan/qa/).

Its first recommendations are to clear the Low Value Content name for trademark, secure the domain and social handles, and select the six launch sayings before any broader disclosure. That is why this repository is private.

## Documentation

| Document | Location |
| --- | --- |
| Business plan | [docs/business-plan/](docs/business-plan/) |
| Concept catalog | [docs/product/concept-catalog.md](docs/product/concept-catalog.md) |
| Ecosystem apparel catalog | [docs/product/ECOSYSTEM_APPAREL_CATALOG.md](docs/product/ECOSYSTEM_APPAREL_CATALOG.md) |
| Master apparel manifest | [docs/product/apparel-manifest.md](docs/product/apparel-manifest.md) |
| Agent and ChatGPT project notes | [AGENTS.md](AGENTS.md) |
| Change history | [CHANGELOG.md](CHANGELOG.md) |

## Quality and security

| Check | Where | What it does |
| --- | --- | --- |
| Site and config checks | CI (`scripts/check-site.py`) | Every page has `lang`, title, viewport, and description; local links and assets resolve; Firebase JSON is valid |
| Secret scan | CI (gitleaks, full history) | Fails on committed keys, tokens, or private keys |
| Promotion guard | CI, pull requests | Fails PRs that skip an environment (advisory; see below) |
| Pipeline Summary | CI | Single pass/fail roll-up of the checks above |
| Dependabot | GitHub | Alerts, security updates, and weekly GitHub Actions updates |

The organization is on the GitHub Free plan, so this private repository cannot use branch protection, secret scanning, or code scanning. CI covers what it can; the promotion flow is enforced by convention. See [SECURITY.md](SECURITY.md).

## Contributing, security, and support

- [CONTRIBUTING.md](CONTRIBUTING.md): workflow and standards
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): expected behavior
- [CLAUDE.md](CLAUDE.md): guide for AI-assisted sessions
- [SECURITY.md](SECURITY.md): reporting vulnerabilities
- [SUPPORT.md](SUPPORT.md): where to get help

## License

Copyright © 2026 Nelson Grey LLC. All rights reserved. This is proprietary material; see [LICENSE](LICENSE).
