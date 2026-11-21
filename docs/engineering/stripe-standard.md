# Nelson Grey Stripe standard

Status: adopted November 10, 2026. Applies to Low Value Content, Vehicle Vitals and Wishlist Wizard. No customers existed at adoption, so every product was brought to the standard at once rather than migrated gradually.

## Why a standard

Each product had grown its own Stripe wiring: hand-written HTTP calls in one, five differently pinned SDK clients in another, price ids copied into secrets per environment, webhook URLs pointing at raw `cloudfunctions.net`. Every environment drifted differently, and drift was found by accident. The rules below remove the sources of drift, and `tools/stripe/` detects what remains.

## Accounts and environments

| Environment | Stripe | Firebase project suffix |
|---|---|---|
| dev | "NG Sandbox dev" sandbox | `-dev` |
| staging | "NG Sandbox staging" sandbox | `-staging` |
| prod | live mode | `-prod` |

- All products share one Stripe account per environment. Separate products are told apart by `metadata.app` (see below), product names and lookup keys, never by separate accounts.
- Split into a separate account only where a product's risk or regulatory profile differs. Wishlist Wizard's Connect payouts are the likely candidate. Do not split for branding alone.
- The account-level support email is `support@nelsongrey.com` and the support URL is `https://nelsongrey.com/support`. Per-product addresses (`support@lowvaluecontent.com`, `support@vehicle-vitals.com`, `support@wishlist-wizard.com`) belong on each product's own pages and app copy. Stripe holds only one address per account.
- The legacy "Test mode" account is scratch only. Nothing may depend on it.
- Live mode is never touched by tooling. Going live is a deliberate, separate step.

## Rules

1. **One client module per service.** Every Stripe call goes through a single module (`stripe-client.ts`, `stripe/client.ts`). It uses the official `stripe` package, the same major version in every repo, and **one pinned `apiVersion`** equal to the SDK's own. No hand-written HTTP calls, and no `require('stripe')` scattered through the code.
2. **The webhook endpoint's `api_version` equals the pinned client version.** Webhook payloads follow the endpoint's version, not the client's. A mismatch silently changes event shapes (for example `invoice.subscription` versus `invoice.parent.subscription_details`). An endpoint's `api_version` cannot be edited, so a mismatch means recreate the endpoint. `stripe_reconcile.py audit` checks this.
3. **Webhook URL.** `https://<site domain>/api/webhooks/stripe`, served through the site's own hosting rewrite. Never `cloudfunctions.net`. One endpoint per product per environment.
4. **Webhook handling.** Verify with the SDK (`constructEvent`) against the raw body, with the default 5 minute tolerance. De-duplicate by `event.id`. Return 2xx for event types we do not handle. Return non-2xx only when we want Stripe to retry (for example an event whose user is not mapped yet because the checkout event has not been processed). Release the dedupe claim if processing fails so the retry is applied.
5. **Prices by lookup key.** Lookup keys are `<TIER>_WEB_<MONTH|ANNUAL>` (for example `PLUS_WEB_MONTH`). Code resolves prices with `prices.list({ lookup_keys })`. **Price ids are never stored in secrets or config**, because they differ in every environment and were the main source of drift. One-time products (Low Value Content) price inline from the server catalog.
6. **Portal configuration by name.** Each subscription product has a billing portal configuration named for the product (`VEHICLE-VITALS`, `WISHLIST WIZARD`), resolved by name at runtime. No portal id in config.
7. **Secrets.** `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` in Secret Manager. Prefer a restricted key (`rk_`) with only the permissions the service needs. URLs and ids are plain configuration, not secrets.
8. **Idempotency.** A Checkout request uses its own random order token as the Stripe idempotency key. A Stripe network retry of that request is safe, and separate buyers can never share a session because they ordered the same basket at the same time. Browser checkout buttons disable while the request is in flight.
9. **Metadata.** Every object created carries `metadata.app` (`low-value-content`, `vehicle-vitals`, `wishlist-wizard`) and `metadata.env` (`dev`, `staging`, `prod`).
10. **Declared state.** The desired products, prices, webhook events, endpoints and portal settings live in `tools/stripe/manifest.json`. Change Stripe by changing the manifest and running the tool, not by clicking around.

## Tooling

```sh
python3 tools/stripe/stripe_reconcile.py audit              # read-only, exits 1 on drift
python3 tools/stripe/stripe_reconcile.py apply --env dev    # fix what Stripe allows in place
python3 tools/stripe/stripe_reconcile.py apply --create-webhooks --env dev --product vehicle-vitals
```

Keys come from `functions/.secret.local` (gitignored, prefixes `SANDBOX_DEV_`, `SANDBOX_STAGING_`). The tool refuses any key that is not a test key. It creates an endpoint's signing secret into the same file, never to the terminal.

## Rolling the standard out to an environment

Order matters, because Stripe must never call a route that does not exist yet.

1. Merge and deploy the product's code (functions and hosting) to the environment.
2. Create the new endpoint with `apply --create-webhooks`, so it has the correct URL, events and `api_version`.
3. Store its signing secret as a new version of `STRIPE_WEBHOOK_SECRET` in Secret Manager and redeploy the function so it binds the new version. Cloud Run pins secret versions, so a redeploy is required.
4. Send a test event and confirm a 2xx and the expected state change.
5. Delete the old endpoint.
6. Retire the now-unused secrets (`STRIPE_PRICE_ID_*`, `STRIPE_PORTAL_CONFIGURATION_ID`).

## Known open items at adoption

- **Wishlist Wizard Connect events.** Its endpoint subscribes to `account.updated`, which a platform endpoint only receives for connected accounts through a separate Connect endpoint (`connect: true`). Decide whether to add one when payouts launch.
- **Vehicle Vitals period field.** The `customer.subscription.deleted` handler reads `current_period_end` from the subscription. In current API versions that field is on the subscription items, so cancellations fall back to "now". Harmless today, worth fixing.
- **Tax.** Wishlist Wizard enables automatic tax on checkout. Low Value Content sets `txcd_99999999` (tangible goods) on every line and `txcd_92010001` (shipping) on the shipping rate, both tax-exclusive, in `functions/src/checkout.ts`. Dev and staging each have an active Illinois sandbox registration and `STRIPE_AUTOMATIC_TAX=true`; the November 20 dev test calculation returned `standard_rated` for apparel and `product_exempt` for shipping. Vehicle Vitals and Wishlist Wizard are subscriptions and need their own codes on their Stripe Products (accountant to confirm Illinois treatment). Registrations are per Stripe mode. The live Illinois registration's ID is masked in Dashboard and has not been matched to an IDOR Sales/Use registration; do not enable live tax or checkout until it is corrected and verified.
- **Support URL, dev sandbox.** Currently `https://www.nelsongrey.com/support`; the manifest expects no `www`. Dashboard-only setting.
- **Live mode.** The Nelson Grey LLC account is accessible. Low Value Content now has a Checkout Sessions Write restricted key and a four-event live webhook; the key and Printify API token are in production Secret Manager. The Stripe signing secret and function deployment remain. The live endpoint uses `2026-11-18.endive` because Dashboard did not offer the SDK's pinned `2026-10-28.endive`; verify compatibility or align versions before the first live order. The account's Illinois Tax location is marked `Needs attention`; its masked ID ends `707`, which could be the LLC file number previously used in error. Confirm the full number against IDOR before launch. Production remains on the coming-soon page with checkout disabled.

## Rollout status

| Environment | Low Value Content | Vehicle Vitals | Wishlist Wizard |
|---|---|---|---|
| dev | Done November 20, 2026. Billing and functions active; six-product checkout deployed; paid Stripe sandbox session created one Printify order on hold, then the test order was canceled and the status webhook updated Firestore. Signed webhooks and duplicate Stripe delivery verified. Printify shop approval is Manual. | Done November 10, 2026. New endpoint verified with a Stripe-signed event; old endpoint deleted | Done November 10, 2026. New endpoint verified; duplicate delivery de-duplicated; old endpoint deleted |
| staging | Stripe webhook and active Illinois sandbox registration verified November 21; full end-to-end order flow still to test. | Not started | Not started |
| prod / live | Checkout key, webhook destination, Printify API token and Printify webhook secret configured Nov 21; backend, Stripe signing secret, and tax correction remain. | Not started | Not started |

Staging follows the normal promotion flow (`develop` to `staging`), then the rollout steps above against the staging sandbox.
