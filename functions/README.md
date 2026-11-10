# Commerce functions

Stripe Checkout, Printify production, and a Firestore order ledger. Hosting rewrites `/api/**` to the `api` function; a scheduled `reconcile` function retries stuck orders.

## Flow

1. Browser `POST /api/checkout-session` with `{items:[{productId, variantId, quantity}]}`. Prices and Printify IDs come only from [src/catalog.ts](src/catalog.ts).
2. Stripe collects payment, email, phone and a US shipping address.
3. A verified Stripe webhook marks the order `paid`, then submits it to Printify with the Checkout Session ID as `external_id`.
4. The Printify order stays **on hold**: it is created but not sent to production until approved in the Printify dashboard (or `PRINTIFY_AUTO_APPROVE=true`).
5. Verified Printify webhooks advance the status (`in_production`, `shipped` with tracking, `delivered`). Status never moves backwards.
6. Customers see status at `/order?token=…` via `GET /api/orders/:publicToken`.

## Order states

`awaiting_payment` → `paid` → `submitting` → `on_hold` → `in_production` → `shipped` → `delivered`.
Side exits: `payment_failed`, `expired`, `canceled`, `fulfillment_error` (Printify rejected the call; safe to retry automatically), `needs_review` (outcome unknown, or amount mismatch; **a human must check Printify for an order with this external_id before retrying**, because Printify cannot be queried by external ID here).

## Setup (per Firebase project)

```sh
firebase functions:secrets:set STRIPE_SECRET_KEY
firebase functions:secrets:set STRIPE_WEBHOOK_SECRET
firebase functions:secrets:set PRINTIFY_API_TOKEN
firebase functions:secrets:set PRINTIFY_WEBHOOK_SECRET
```

Params (prompted on deploy, or in `functions/.env.<project>`): `PRINTIFY_SHOP_ID`, `SITE_URL`, `STRIPE_AUTOMATIC_TAX`, `PRINTIFY_AUTO_APPROVE`.

Stripe webhook endpoint: `https://<site>/api/webhooks/stripe`, events `checkout.session.completed`, `.async_payment_succeeded`, `.async_payment_failed`, `.expired`.
Printify webhooks (register via API with the shared secret): `order:sent-to-production`, `order:shipment:created`, `order:shipment:delivered`, `order:updated` to `https://<site>/api/webhooks/printify`.

Use Stripe **test** keys and a Printify test shop outside production.

## Before it can sell anything

[src/catalog.ts](src/catalog.ts) currently sells only `validate` (No. 01), with a real Printify product and a single variant (`white-l`). The other nine launch designs are not in the catalog, so checkout refuses them. For each design, create the Printify product, then add its product ID and per-size variant IDs here and set the matching `commerce` fields in `docs/product/apparel-manifest.json`; `scripts/check-apparel-manifest.py` verifies the two agree.

## Development

```sh
npm install
npm test          # vitest, no network or Firebase needed
npm run typecheck
```

Unverified assumptions to confirm against a real test event before trusting them: the Printify webhook payload shape (`resource.id`, `resource.data.carrier`) and the `X-Pfy-Signature` header format.
