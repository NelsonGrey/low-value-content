# Contributing to Low Value Content

This is a private, proprietary repository owned by Nelson Grey LLC. Contributions are by invitation only, and all contributed work belongs to Nelson Grey LLC (see [LICENSE](LICENSE)).

## Branches and environments

| Branch | Purpose | Firebase project |
| --- | --- | --- |
| `develop` | Default branch; integration of all new work | `low-value-content-dev` |
| `staging` | Release candidate; final review | `low-value-content-staging` |
| `main` | Production | `low-value-content-prod` |

Work flows one way: `feature/*` → `develop` → `staging` → `main`. Do not commit directly to `staging` or `main`. Pushes to those branches deploy the website automatically (see [README](README.md#deployment)).

## Workflow

1. Branch from `develop`: `git switch -c feature/short-description develop` (use `fix/` for fixes, `docs/` for documentation, `design/` for shirt art).
2. Make focused changes. Keep unrelated changes in separate pull requests.
3. Open a pull request into `develop` and complete the PR template.
4. After review and merge, promote with pull requests `develop` → `staging` → `main`.

Use clear, imperative commit messages ("Add Validate Me shirt prototype"), with a short body when the reason is not obvious.

## What belongs in git

Source, designs, docs, tools, and the website source (`website/`) are tracked. Never commit credentials, service-account keys, API tokens, or `.env` files. GitHub rejects files over 100 MB.

If a local `sources/` folder exists, it is a read-only mirror of the original ChatGPT project (it is not tracked in git). Do not edit, rename, move, or delete anything in it (see [AGENTS.md](AGENTS.md)).

## Content and naming

- Slogans in the [concept catalog](docs/product/concept-catalog.md) are not trademark-cleared. Do not present them as cleared in copy, listings, or the website.
- Keep satire aimed at online behavior and platforms, not at individuals or protected groups.

## Checks

Before opening a pull request, run `python3 scripts/check-site.py` (after a build), `python3 scripts/check-apparel-manifest.py` and, if you touched config or secrets handling, `gitleaks detect --source . --redact`. CI runs the same checks, a secret scan, and an advisory promotion guard that fails pull requests which skip an environment (`develop` → `staging` → `main` only). Branch protection is not available on this plan, so follow the flow by hand.

## Website

- The site is an Astro project in `website/` (Node 24+). Run `npm run build --prefix website` to generate `website/dist/`, which is not committed.
- Check pages at mobile and desktop widths and keep contrast accessible.
- Test locally with `firebase emulators:start --only hosting` or any static server.

## Tools

- Python 3.11+. The business plan is regenerated with `python tools/business-plan/build_business_plan.py`.
- Scripts should resolve paths from the repository root and avoid absolute paths.

## Questions

See [SUPPORT.md](SUPPORT.md).
