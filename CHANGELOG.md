# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- Nos. 07–10 now use the ornate full-colour artwork plates across the manifest, storefront, shop proof sheet, and production docs; the retired line art is kept as `legacyArtwork`. Product pages label the plates "not yet print-ready".
- Storefront scripts and styles are external files, so the dev and staging Content-Security-Policy no longer blocks the menu, calendar highlight, or page styles. `scripts/check-site.py` now fails on inline scripts, styles, and `style=` attributes in the built site.
- Product price on the storefront is read from the manifest instead of being hard-coded.

### Fixed
- Cancelling Stripe Checkout returns to `/shop` instead of the nonexistent `/shirts#validate`.
- Shop copy now matches the collection counts (4 Public Notices, 4 Court & Orders, 2 Royal Commemorations).

### Added
- Astro storefront for the Royal House of Engagement (Realm, Lineage, Royal Calendar, ten product pages) generated from the master apparel manifest.
- Repository standards: CI (site checks, gitleaks secret scan, advisory promotion guard, Pipeline Summary), CLAUDE.md, expanded SECURITY policy, `.gitattributes`, `.gitleaks.toml`, grouped Dependabot, meta descriptions on legal pages, and a filled-in GitHub About section.
- Commerce backend (`functions/`): Stripe Checkout sessions, verified Stripe and Printify webhooks, idempotent Printify order submission held for manual approval, Firestore order ledger, public order-status endpoint, and scheduled reconciliation. Test-mode vertical slice on the Drop 001 "validate" shirt; checkout refuses placeholder Printify IDs.
- Branded coming-soon page for production, controlled by the `SHOW_COMING_SOON` environment variable.
- Keyless deploys via Workload Identity Federation (org policy forbids service-account keys).
- Google sign-in access gate on dev and staging with domain and exact-email allowlists (parity with vehicle-vitals).

## [0.1.0] - 2026-10-13

### Added
- Initial project: business plan, concept catalog, shirt prototypes, and launch mockups.
- Firebase Hosting for `dev`, `staging`, and `prod` environments with a placeholder landing page.
- GitHub repository under NelsonGrey with `develop`, `staging`, and `main` branches.
- GitHub Actions workflow deploying the website per branch.
- Repository documentation: LICENSE, CONTRIBUTING, SECURITY, SUPPORT, CODE_OF_CONDUCT, issue and PR templates, CODEOWNERS, Dependabot, EditorConfig.
