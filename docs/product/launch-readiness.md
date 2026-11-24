# Launch readiness: everything that has to be true before the holiday six go live

Status: checklist begun **November 11, 2026**; the verified update below is from **November 21, 2026**. This is the working checklist behind [holiday-launch-plan.md](holiday-launch-plan.md). Update the state column as work lands. Going live is a separate release step.

## Verified November 21 update

- The IDOR REG-1 email supplied for Nelson Grey LLC lists **only IL Business Income Tax** with account ID `20670-81248`. It does not establish a Sales/Use Tax retailer or reseller registration. The `D18371707` number in local business notes is labeled an Illinois LLC file number. Neither is evidence of an Illinois resale account ID. The previously submitted Printify MTC certificate used `18371707` and must not be relied on; ask Printify to withdraw or replace it when the correct IDOR registration is available.
- Stripe's dev and staging sandboxes each have an active Illinois tax registration and the Low Value Content Checkout webhook is present with the expected four events. These are sandbox records, not proof of an IDOR registration.
- Live Stripe Tax shows an Illinois registration marked **Needs attention**. Its masked ID ends `707`, which may match the LLC file number; verify the full ID and correct the registration before enabling live automatic tax. Stripe's notice says its setup for subscriptions, invoices and payment links is incomplete; that notice does not by itself establish whether this Checkout integration can collect tax.
- Production Firebase has billing, Hosting and the coming-soon page. The required Cloud Functions, Cloud Run, Cloud Build, Artifact Registry, Cloud Scheduler, Eventarc and Secret Manager APIs are enabled. Live Stripe Checkout and Printify API credentials are stored in production Secret Manager; the Stripe webhook signing secret awaits Google Cloud Console verification. No production commerce backend is deployed. The `production` GitHub Environment has `SHOW_COMING_SOON=true`.
- The development and staging preview screens are a client-side Google/Firebase gate. Hosting still serves their files to anyone who knows the URLs; a server-side access policy is needed if the preview content must be genuinely private.

State key: **Done** (built and checked), **Ready** (I can do it now without a decision), **Needs Mark** (a decision, money or an account action), **Needs outside** (accountant, counsel, Printify, Stripe), **Blocked** (waits on a sample or an earlier item).

## 1. Product and art

| Item | State | Notes |
|---|---|---|
| Six approved redesigns, outlined SVG plus 4500 x 5400 PNG | Done locally | `production/print-files/launch-six-redesign-candidate-v1/`; mechanical QA and a proof sheet passed November 23. **Local-only (gitignored)**; physical sample and provider acceptance remain open. The November 11 backup contains the earlier art, not this redesign. |
| Editable sources and fonts | Done | `design/launch-six/` |
| Garment colors locked to real blank names | Done | Manifest `blankColor` plus checker; Brick provisional |
| Confirm Brick and True Navy on a real shirt | Blocked | Needs samples |
| Confirm print quality, thin rules and gold on dark cotton | Blocked | Needs samples |
| Frame and small-type quality on the redesign | Blocked | At the 0.82 placement the thinnest rules are about 0.030 in, exactly on the local 0.03 in target with no margin. Confirm edge quality and small serif text, especially the maker's line (about 8 pt capitals), on a physical sample. |
| Trademark knockout searches for the six sayings and the brand | Needs outside | Cannot be done from here; search the USPTO and common marketplaces; the site must not claim clearance |

## 2. Printify

| Item | State | Notes |
|---|---|---|
| Six draft products (Ivory, True Navy, Brick; S to 3XL; placed art) | Done | Existing drafts received the redesign and maker's line November 23, then shortened to x 0.50, y 0.42, scale 0.82, shortened further to y 0.39, scale 0.75, and restored to x 0.50, y 0.42, scale 0.82 the same day (at 0.75 the thinnest rules printed at 0.028 in, under the 0.03 in target). Each read-back verified image IDs, price, variants and placement. Logs: `production/qa/printify-redesign-update-2026-11-23-first-pass.json`, `production/qa/printify-redesign-update-2026-11-23.json`, `production/qa/printify-placement-update-2026-11-23.json`, and `production/qa/printify-placement-update-2026-11-23-v2.json`. |
| Old test product removed | Done | Deleted November 11 |
| Prices on the Printify products | Done | Set to $36 on November 11 |
| Confirm real production time and the holiday cutoff | Needs outside | Ask Printify support or read the provider page; the 10-day API field looks like a default |
| Printify Premium plan: price and discount | Needs outside | Could save about $2.50 per shirt; check the current terms |
| Resale certificate so Printify stops charging tax | Blocked | Correct IDOR Sales/Use retailer or reseller account ID is not yet evidenced. The submitted MTC used the LLC file number; replace or withdraw it. Do not treat a Printify approval of that document as tax clearance. |
| Webhook registration for shipped and delivered events | Partly done | Dev and staging each have four signed order-event subscriptions. Production registration follows backend deployment; live payload shape still unverified. |
| Publish to a sales channel | Not needed | The site sends orders by API; the drafts stay unpublished |
| Sample order (4 shirts, about $69) | **Needs Mark** | Mark decides when everything else is built |

## 3. Storefront and backend

| Item | State | Notes |
|---|---|---|
| Homepage and site-wide 1280px layout | Done | Audited with `tools/site-qa` (screenshots, axe, layout rule, Lighthouse). Preview renders are interim product images; replace with sample photography |
| Product pages, cards, shop page for the six | Done | Real blank color shown on each page. The site lists and builds only the six (`holidayLaunch`); Nos. 07 to 10 are hidden |
| Catalog with variants and Printify ids | Done | `functions/src/catalog.ts`, matched to the manifest by the checker |
| Final price in catalog, Stripe line item, manifest and Printify | Done | $36, applied November 11; guarded by the manifest checker |
| Tiered shipping | Dropped | Mark chose flat $5.99 on Nov 23 |
| Cart and checkout copy for a real launch (remove "Test configuration" notes) | Done in launch branch | $5.99 flat US shipping, tax at checkout, and returns link. Keep aligned with any future shipping decision. |
| Order status page and emails | Ready | Page exists; transactional email (order confirmation, shipping) is not built |
| Deploy to dev and run test orders for all six | Ready | After the PR merges |
| Deploy to staging and repeat | Done Nov 23 | Staging was promoted from `develop` (PR #72; website matches the repo, verified by hash) and its functions were redeployed from a clean `staging` checkout (34 tests, 0 vulnerabilities). The staging checkout now shows the corrected No. 04 name, and `reconcile` runs every 30 minutes with no errors since the Firestore index (PR #61). Paid sandbox order Nov 23: tax on the apparel line only, Printify order created on hold, then cancelled. The order-status page after payment has not been seen (staging sign-in gate). |
| Failure-path tests (declined card, expired session, Printify error) | Partly done | Run live on staging Nov 23: 22 HTTP cases pass (invalid JSON, wrong content type, unknown product or size, quantity 0, 6, 1.5 and negative, 7 lines, forged or missing Stripe and Printify webhook signatures, junk and unknown order tokens); a declined card (4000 0000 0000 0002) shows Stripe's "Your card was declined", keeps the shopper on checkout with tax still correct and creates no Printify order; backing out of checkout returns to `/shop`. Unit tests cover payment failure and expiry, duplicate delivery, and Printify rejection (500 so Stripe retries) and ambiguous failures (parked for review). **Not run live:** an expired session and a real Printify API error. Minor: malformed JSON gets Express's default HTML 400 page rather than JSON (the cart still shows its friendly message). |
| Product images: Printify mockups as interim, sample photos later | Done locally | November 23 generated mockups for the approved redesigns replaced the six storefront mockup files, and were regenerated after the maker's line was added; sample photos remain open. The small maker's line on dark garments needs checking on the physical sample. |
| Size chart and fit copy | Ready | Take measurements from the Printify blueprint and the sample |

## 4. Legal and policy

| Page | State | Notes |
|---|---|---|
| Terms of sale | Drafted in launch branch, Needs outside | Includes purchase, shipping, returns, and contact terms; counsel review before live payments |
| Privacy | Drafted in launch branch, Needs outside | Describes Stripe, Printify, Firebase, order records, and dev/staging sign-in |
| Cookies | Drafted in launch branch | Cart local storage and external checkout disclosed; no public ad or analytics cookies |
| Shipping policy | Drafted in launch branch | US only, $5.99 per order, variable production and delivery times; revisit if tiered shipping is approved |
| Returns and replacements | Approved by Mark, drafted | Revised Nov 23: fit returns accepted (30 days, unworn, item refund or size exchange, customer pays return shipping); photo within 30 days for damage, misprint, or wrong item; replacement or refund. Pages: `returns.astro`, `shipping.astro`, terms, support |
| Support page with contact | Approved by Mark, drafted | `support@lowvaluecontent.com` is monitored |
| Trademark-cleared language | Needs Mark | Keep "not cleared" language off the customer-facing site, but never claim clearance |

**Returns policy (revised Nov 23, Mark decided to accept fit returns):** fit returns and size exchanges within 30 days of delivery, unworn and unwashed, item price refunded, customer pays return shipping. Damage, misprints and wrong items: free replacement or refund with a photo within 30 days. Cost note: Printify does not take back fit returns, so each one is a loss to us; offer exchanges first and publish a size chart. Applicable legal rights still apply.

## 5. Money and tax

| Item | State | Notes |
|---|---|---|
| Shipping decision | Done | Mark decided Nov 23: flat $5.99 per order, US only |
| Sales-tax collection (nexus, Stripe Tax) | Blocked for live | Checkout sends tax codes (apparel `txcd_99999999`, shipping `txcd_92010001`, tax-exclusive). Sandbox Illinois registrations are active. The live registration's number must be verified against an actual IDOR Sales/Use account before live collection. Other states: accountant. |
| Stripe live account structure (one account for the LLC, Connect isolated for Wishlist Wizard if needed) | Needs Mark | See `docs/engineering/stripe-standard.md` |
| Live product catalog and webhook for Low Value Content | Partly done | Least-privilege Checkout key and four-event webhook destination created. Backend and webhook signing secret remain; live checkout stays disabled until tax and policy gates are satisfied. The live webhook is `2026-11-18.endive`, while the SDK is pinned to `2026-10-28.endive`; verify compatibility or align before live orders. |
| One real live order, then refund | Blocked | After live mode |
| Printify billing method and spending limit | Needs Mark | Check the funding source before the first real order |

## 6. Marketing and launch operations

| Item | State | Notes |
|---|---|---|
| Social kit (58 feed cards, schedule) | Partly done | Product cards for the six were regenerated November 11 (`tools/social/build_social.py --only product`). The posting schedule and captions still reflect the old plan (No. 07 on Nov 20, "not yet for sale" copy); re-plan once the launch date is set |
| Social accounts and handles | Needs Mark | Not created |
| Email capture or waitlist | Ready | Not built; propose a simple form that posts to a Firestore collection, with a consent line |
| Launch announcement copy and a "last order for Christmas" banner | Ready | Banner date waits on the provider's cutoff |
| Analytics | Needs Mark | None installed; decide whether to add privacy-friendly analytics (affects the cookie and privacy pages) |

## 7. Release mechanics (never done without Mark's explicit go)

1. PR `feature/holiday-six-storefront` into `develop` (merge deploys dev).
2. Test orders on dev for all six, then `develop` into `staging` and repeat.
3. Samples approved; colors and art adjusted if needed.
4. Live Stripe configured; one real order and refund.
5. Set `SHOW_COMING_SOON=false` in the `production` GitHub Environment and promote `staging` into `main`.
6. Watch the first orders: Stripe, the order ledger, Printify and the customer email.

## Open questions I cannot answer from here

- The real Printify production time and holiday cutoff.
- Whether Brick looks right on a shirt.
- Competitor price points (Etsy, Threadless, Cotton Bureau).
- Whether Printify tax can be exempted.
- How the "shipped" and "delivered" webhooks are shaped.
