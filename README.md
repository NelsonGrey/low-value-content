# Low Value Content

[![Deploy Website](https://github.com/NelsonGrey/low-value-content/actions/workflows/deploy-website.yml/badge.svg)](https://github.com/NelsonGrey/low-value-content/actions/workflows/deploy-website.yml)
![License: Proprietary](https://img.shields.io/badge/license-proprietary-lightgrey)

**Low Value Content** is a satirical t-shirt brand of **Nelson Grey LLC**. The shirts poke fun at social media theater, algorithm anxiety, the creator economy, and other symptoms of being extremely online.

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
- [Branching and releases](#branching-and-releases)
- [Business plan](#business-plan)
- [Documentation](#documentation)
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
│   └── product/            Concept catalog and other product notes
├── design/
│   ├── prototypes/         Shirt design SVGs and PNG previews
│   └── mockups/            Launch mockup images
├── tools/
│   └── business-plan/      build_business_plan.py (regenerates the .docx)
├── website/
│   └── dist/               Deployed static site (Firebase Hosting)
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

The site is plain static HTML in [website/dist/](website/dist/) with no build step yet. The framework has not been chosen; when it is, scaffold it in `website/` and point `hosting.public` in [firebase.json](firebase.json) at the build output.

Preview locally:

```bash
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

[.github/workflows/deploy-website.yml](.github/workflows/deploy-website.yml) deploys on every push to `develop`, `staging`, or `main` that changes `website/dist/**`, `firebase.json`, or `.firebaserc`. Each branch maps to its own GitHub Environment (`development`, `staging`, `production`).

Each environment needs a secret named `FIREBASE_SERVICE_ACCOUNT` containing the service-account JSON for that environment's Firebase project. Deploys fail until these are set.

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
| Agent and ChatGPT project notes | [AGENTS.md](AGENTS.md) |
| Change history | [CHANGELOG.md](CHANGELOG.md) |

## Contributing, security, and support

- [CONTRIBUTING.md](CONTRIBUTING.md): workflow and standards
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): expected behavior
- [SECURITY.md](SECURITY.md): reporting vulnerabilities
- [SUPPORT.md](SUPPORT.md): where to get help

## License

Copyright © 2026 Nelson Grey LLC. All rights reserved. This is proprietary material; see [LICENSE](LICENSE).
