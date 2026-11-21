# Go-live runbook: from "resale certificate approved" to live

Status: updated **November 21, 2026**. Companion to [launch-readiness.md](launch-readiness.md) section 7. Production still serves the coming-soon page. The November 21 request authorizes preparation of the environments; opening public checkout remains gated on verified tax registration, corrected Printify exemption, policies, and an end-to-end live order.

## Where each environment stands

| | Website | Access gate | Stripe | Backend (functions, Firestore) |
|---|---|---|---|---|
| dev | Current `develop` | Storefront look, deployed | Sandbox. Illinois registration active, `STRIPE_AUTOMATIC_TAX=true` | Deployed and verified end to end |
| staging | Current `develop` (promoted Nov 20) | Storefront look, deployed | Sandbox. Illinois registration active; webhook matches expected events/version | `api` and `reconcile` deployed; verify their exact revisions and run a complete sandbox order before promotion |
| prod | Coming-soon page | Not gated, by design | Live Illinois Tax location needs attention; masked account ID ends `707` and is not verified against IDOR. Four-event live webhook created. | Billing and Firestore on; required APIs enabled. Stripe Checkout key, Printify API token, and Printify webhook secret stored. Stripe signing secret and functions deployment remain. `CHECKOUT_ENABLED=false` in local prod config |

## What the resale certificate does and does not gate

An accepted Illinois resale certificate can stop **Printify** charging us tax on qualifying purchases. It does not register Nelson Grey LLC to collect sales tax from customers. The IDOR email currently available lists only **IL Business Income Tax** (`20670-81248`); the previously submitted MTC certificate used the LLC file number (`18371707`). Obtain and verify the IDOR retailer/reseller Sales/Use Tax account ID, correct the Printify submission and Stripe's live registration, then confirm the exemption is approved before public sales.

## A. Staging: finish before anything else

1. From a clean checkout of `staging`: `firebase deploy --only functions --project low-value-content-staging`. `functions/.env.low-value-content-staging` has `STRIPE_AUTOMATIC_TAX=true` and `CHECKOUT_ENABLED=true`.
2. Confirm Firebase CLI authentication before deploying; refresh it interactively if it has expired.
3. Verify: the `api` revision is newer than Nov 10, the `STRIPE_AUTOMATIC_TAX` env var reads true, and a sandbox test order shows tax on the apparel line and none on shipping.
4. Repeat the failure-path tests from launch-readiness section 3 (declined card, expired session, Printify error).

## B. Production, in order

Preparation is authorized by Mark's November 21 request. Keep `CHECKOUT_ENABLED=false` and `SHOW_COMING_SOON=true` throughout preparation.

1. **GCP project** (`low-value-content-prod`). Follow the new-project list: enable the Cloud Functions, Cloud Run, Cloud Build, Artifact Registry and Secret Manager APIs; grant the compute service account `roles/cloudbuild.builds.builder` and `roles/datastore.user`; apply the project-level org-policy override for public invoker access, then bind `allUsers` to `roles/run.invoker` on `api`.
2. **Live Stripe.**
   - Activate the live account (structure decision in [stripe-standard.md](../engineering/stripe-standard.md)).
   - Verify the actual IDOR Sales/Use Tax registration. Correct the live Illinois Tax account ID; its current masked value ends `707` and may be the LLC file number. Confirm tax settings and the head-office address.
   - The webhook endpoint `https://lowvaluecontent.com/api/webhooks/stripe` was created Nov 21 with four checkout events. The Dashboard offered `2026-11-18.endive`; the SDK is pinned to `2026-10-28.endive`. Align or verify this version difference before live orders.
   - `STRIPE_SECRET_KEY` is a Checkout Sessions Write restricted key. `PRINTIFY_API_TOKEN` and `PRINTIFY_WEBHOOK_SECRET` are stored in Secret Manager. Store the live `STRIPE_WEBHOOK_SECRET` after Cloud Console sign-in.
   - Set the account support email to `support@nelsongrey.com`.
3. **Prod config.** `functions/.env.low-value-content-prod` is gitignored and has `SITE_URL=https://lowvaluecontent.com`, `PRINTIFY_SHOP_ID=29342324`, `STRIPE_AUTOMATIC_TAX=false`, `CHECKOUT_ENABLED=false`, and `PRINTIFY_AUTO_APPROVE=false`. Only set automatic tax and checkout true after the correct registration is verified and the live tax calculation is tested. Recheck the Printify shop's Manual approval setting immediately before a real order.
4. **Deploy functions** to prod from a clean `main` checkout, and register the Printify webhooks.
5. **Rehearse behind the curtain.** When the tax registration and policies are resolved, temporarily enable checkout for one controlled live order while production Hosting still shows coming soon. Confirm Stripe, the order ledger, Printify and tax; refund the payment and restore checkout disabled until public launch. A live Printify order is not simulated and must be canceled or fulfilled deliberately.
6. **Open the doors.** Open a PR `staging` into `main` (approve in the `production` environment), then set the `SHOW_COMING_SOON` variable in the `production` GitHub Environment to exactly `false` and re-run the deploy. Watch the first orders.

## Before step 6, decisions still open

The site now uses $5.99 flat US shipping and has draft customer policy pages with Mark's approved returns terms and monitored support address. Counsel review, real production time and holiday cutoff from Printify, a sample shirt order, and transactional email remain. See launch-readiness sections 2 to 5.

## Rolling back

Set `SHOW_COMING_SOON` back to `true` and re-run the `main` deploy. The coming-soon page returns in about a minute. This does not cancel orders already placed.
