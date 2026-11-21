# Security Policy

## Supported Versions

Low Value Content has not launched. Only the code currently on each environment branch is supported; there is no long-term support for older commits.

| Branch | Environment | Status |
|---|---|---|
| `main` | Production (coming-soon page) | Supported |
| `staging` | Staging | Supported |
| `develop` | Development (default branch) | Supported |

## Reporting a Vulnerability

This repository is private and has no public issue tracker, so please don't report security concerns through issues or pull requests. Email **admin@nelsongrey.com** with:

- A description of the vulnerability and its potential impact
- Steps to reproduce, or a proof of concept if available
- Any relevant logs, request and response samples, or affected URLs

You should get an acknowledgement within a few business days.

## Scope

- The Low Value Content website (`website/`, including `website/coming-soon/`) and its Firebase Hosting deployments
- The non-production access gate (`website/public/assets/auth-gate.js`) and its allowlist handling
- GitHub Actions workflows, Workload Identity Federation deploy configuration, and hosting headers
- Accidentally exposed secrets or personal data in the repository

## Security Model

- **Non-production gating:** dev and staging require Google sign-in from an allowlisted domain or email, and send `X-Robots-Tag: noindex, nofollow, noarchive` plus a strict Content Security Policy. The gate keeps the public out; it is not a hard authentication boundary, because the allowlist ships in the page.
- **Keyless deploys:** GitHub Actions authenticates to Google Cloud with Workload Identity Federation. Each Firebase project trusts only this repository and only that environment's branch. No service-account keys exist.
- **No data collection:** the website has no forms, accounts, or analytics.

## Dependency and Secret Hygiene

Dependabot alerts, security updates, and version updates are enabled. CI runs a gitleaks secret scan on every push and pull request. Do not commit credentials; deploy configuration lives in GitHub Environment secrets and variables, never in source.

GitHub secret scanning, push protection, code scanning, private vulnerability reporting, and branch protection are not available for this repository because it is private on the GitHub Free plan. The gitleaks CI job and the advisory promotion guard stand in for them until the plan changes.
