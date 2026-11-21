# Go-live runbook: from "resale certificate approved" to live

Status: current as of **November 20, 2026**. Companion to [launch-readiness.md](launch-readiness.md) section 7. Nothing here has been run against production. Prod still serves the coming-soon page, and the standing rules apply: no push or PR to `main`, no prod deploy, and no live Stripe access without Mark's explicit go.

## Where each environment stands

| | Website | Access gate | Stripe | Backend (functions, Firestore) |
|---|---|---|---|---|
| dev | Current `develop` | Storefront look, deployed | Sandbox. Illinois registration active, `STRIPE_AUTOMATIC_TAX=true` | Deployed and verified end to end |
| staging | Current `develop` (promoted Nov 20) | Storefront look, deployed | Sandbox. Illinois registration added Nov 20; test calculation: 9% on the $36 shirt ($3.24), shipping exempt | Redeployed Nov 20 (revision `api-00002-map`): six-product catalog, tax codes, `STRIPE_AUTOMATIC_TAX=true`. A sandbox checkout session came back with automatic tax enabled. A paid test order and the failure paths are still to do |
| prod | Coming-soon page | Not gated, by design | Live mode not touched | **Not set up.** Billing is on and Firestore exists. Functions, Cloud Run, Cloud Build and Secret Manager APIs are not enabled, and there are no secrets |

## What the resale certificate does and does not gate

The Illinois resale certificate only stops **Printify** charging us tax on blanks. It does not change anything in the site, Stripe or the backend. It is the business trigger for going live, not a technical dependency, so every step below can be done before it is approved.

## A. Staging: deployed; remaining checks

Steps 1 and 2 were done Nov 20. They are kept as the recipe for prod.

1. Log in: `firebase login` (the CLI login expired; it cannot be done from an automated session).
2. From a clean checkout of `staging` (not a dirty working tree): `firebase deploy --only functions --project low-value-content-staging`. `functions/.env.low-value-content-staging` already has `STRIPE_AUTOMATIC_TAX=true`.
3. Verify: the `api` revision is newer than Nov 10, the `STRIPE_AUTOMATIC_TAX` env var reads true, and a sandbox test order shows tax on the apparel line and none on shipping.
4. Repeat the failure-path tests from launch-readiness section 3 (declined card, expired session, Printify error).

## B. Production, in order

Needs Mark's explicit go for each group; the first two create cloud resources and touch live money.

1. **GCP project** (`low-value-content-prod`). Follow the new-project list: enable the Cloud Functions, Cloud Run, Cloud Build, Artifact Registry and Secret Manager APIs; grant the compute service account `roles/cloudbuild.builds.builder` and `roles/datastore.user`; apply the project-level org-policy override for public invoker access, then bind `allUsers` to `roles/run.invoker` on `api`.
2. **Live Stripe.**
   - Activate the live account (structure decision in [stripe-standard.md](../engineering/stripe-standard.md)).
   - Add the Illinois registration in **live** mode (registrations are per mode) and confirm tax settings and the head-office address.
   - Create the webhook endpoint `https://<prod domain>/api/webhooks/stripe` with `api_version` `2026-10-28.endive` and the four checkout events.
   - Store `STRIPE_SECRET_KEY` (prefer a restricted key) and `STRIPE_WEBHOOK_SECRET`, plus the Printify secrets, in Secret Manager.
   - Set the account support email to `support@nelsongrey.com`.
3. **Prod config.** Create `functions/.env.low-value-content-prod` (gitignored) with `SITE_URL`, `PRINTIFY_SHOP_ID`, `STRIPE_AUTOMATIC_TAX=true` and `PRINTIFY_AUTO_APPROVE`. Decide approval: with Printify's shop setting on Manual, every order waits for a click, which is safer for the first week.
4. **Deploy functions** to prod from a clean `main` checkout, and register the Printify webhooks.
5. **Rehearse behind the curtain.** Prod still shows coming-soon, but the function is live: place one real order and refund it. Confirm Stripe, the order ledger, the Printify order and tax.
6. **Open the doors.** Open a PR `staging` into `main` (approve in the `production` environment), then set the `SHOW_COMING_SOON` variable in the `production` GitHub Environment to exactly `false` and re-run the deploy. Watch the first orders.

## Before step 6, decisions still open

Shipping rule, legal pages (terms, privacy, shipping, returns), real production time and holiday cutoff from Printify, a sample shirt order, and transactional email. See launch-readiness sections 2 to 5.

## Rolling back

Set `SHOW_COMING_SOON` back to `true` and re-run the `main` deploy. The coming-soon page returns in about a minute. This does not cancel orders already placed.
