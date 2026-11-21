# Commerce functions

Stripe Checkout, Printify production, and a Firestore order ledger. Hosting rewrites `/api/**` to the `api` function; a scheduled `reconcile` function retries stuck orders.

## Flow

1. Browser `POST /api/checkout-session` with `{items:[{productId, variantId, quantity}]}`. Prices and Printify IDs come only from [src/catalog.ts](src/catalog.ts).
2. Stripe collects payment, email, phone and a US shipping address.
3. A verified Stripe webhook marks the order `paid`, then submits it to Printify with the Checkout Session ID as `external_id`.
4. The Printify order stays **on hold** when the shop's Order approval setting is **Manual**. `PRINTIFY_AUTO_APPROVE=false` only prevents this function from calling `send_to_production`; it does not override Printify's shop setting.
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

Params (prompted on deploy, or in `functions/.env.<project>`): `PRINTIFY_SHOP_ID`, `SITE_URL`, `STRIPE_AUTOMATIC_TAX`, `CHECKOUT_ENABLED`, `PRINTIFY_AUTO_APPROVE`. Checkout is disabled by default and returns HTTP 503 until `CHECKOUT_ENABLED=true` is set for that project. Keep production false while the resale and tax registrations, policies, and live payment flow are unresolved.

Stripe webhook endpoint: `https://<site>/api/webhooks/stripe`, events `checkout.session.completed`, `.async_payment_succeeded`, `.async_payment_failed`, `.expired`.
Printify webhooks (register via API with the shared secret): `order:sent-to-production`, `order:shipment:created`, `order:shipment:delivered`, `order:updated` to `https://<site>/api/webhooks/printify`.

In dev and staging, use Stripe **test** keys and a Printify shop with **Manual** order approval. Stripe sandbox payments do not make Printify orders simulated; a shop with automatic approval can send them to production and incur a real charge.

## Before it can sell anything

[src/catalog.ts](src/catalog.ts) sells the holiday six (Nos. 01-06), each a real Printify draft product with one garment colour in sizes S-3XL (see `tools/printify/`). Nos. 07-10 are not in the catalog, so checkout refuses them. To add a design, create the Printify product, then add its product ID and per-size variant IDs here and set the matching `commerce` fields in `docs/product/apparel-manifest.json`; `scripts/check-apparel-manifest.py` verifies the two agree.

## Development

```sh
npm install
npm test          # vitest, no network or Firebase needed
npm run typecheck
```

The Printify `X-Pfy-Signature` format and order event payload fields match the current Printify API reference. In dev, a signed webhook probe and Printify's webhook simulator both received HTTP 200 on November 20, 2026; canceling the paid sandbox test order also updated Firestore to `canceled` through a real Printify webhook. Shipment and delivery events still need confirmation against an actual fulfilled order.
