# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Repository standards: CI (site checks, gitleaks secret scan, advisory promotion guard, Pipeline Summary), CLAUDE.md, expanded SECURITY policy, `.gitattributes`, `.gitleaks.toml`, grouped Dependabot, meta descriptions on legal pages, and a filled-in GitHub About section.
- Commerce backend (`functions/`): Stripe Checkout sessions, verified Stripe and Printify webhooks, idempotent Printify order submission held for manual approval, Firestore order ledger, public order-status endpoint, and scheduled reconciliation. Test-mode vertical slice on the Drop 001 "validate" shirt; checkout refuses placeholder Printify IDs.
- Branded coming-soon page for production, controlled by the `SHOW_COMING_SOON` environment variable.
- Keyless deploys via Workload Identity Federation (org policy forbids service-account keys).
- Google sign-in access gate on dev and staging with domain and exact-email allowlists (parity with vehicle-vitals).

### Removed
- Duplicated files at the repository root and in `design-prototypes/`, `mockups/`, `output/`, and two `qa-business-plan*` temp directories; the maintained copies live under `docs/`, `design/`, and `tools/`.

### Changed
- README, brand guide, concept catalog notes, `functions/README.md`, and CONTRIBUTING reflect the ten-design Royal House launch, the real commerce catalog state, and hosting-only CI deploys.
- The business plan builder adds an "Implementation Update" section (ten designs, Stripe and Firebase, Printify hold-for-approval, test-only commerce); the original plan text is unchanged and its QA renders are not regenerated.
- Dependabot now also covers the `website/` and `functions/` npm packages.

## [0.1.0] - 2026-10-13

### Added
- Initial project: business plan, concept catalog, shirt prototypes, and launch mockups.
- Firebase Hosting for `dev`, `staging`, and `prod` environments with a placeholder landing page.
- GitHub repository under NelsonGrey with `develop`, `staging`, and `main` branches.
- GitHub Actions workflow deploying the website per branch.
- Repository documentation: LICENSE, CONTRIBUTING, SECURITY, SUPPORT, CODE_OF_CONDUCT, issue and PR templates, CODEOWNERS, Dependabot, EditorConfig.
