# Holiday 2026 launch plan: the six

Status: current as of **November 11, 2026**. This is the living plan; update it, and its change log at the bottom, whenever anything changes. The detailed work list is in [launch-readiness.md](launch-readiness.md) and the price recommendation is in [pricing-and-cost-analysis.md](pricing-and-cost-analysis.md).

Scope rule: launch small, prove the pipeline end to end, add the next issues in January.

## The six (approved November 10, 2026)

| No. | Saying | Concept | Garment | Printify draft | Art |
|---:|---|---|---|---|---|
| 01 | Please validate me algorithmically. | Progress bar | Ivory | Created | Print master done |
| 02 | Thought leader. No thoughts required. | Door plaque | True Navy | Created | Print master done |
| 03 | I'm not doomscrolling. I'm doing market research. | Field dispatch | Brick | Created | Print master done |
| 04 | Content creator. Uniqueness questionable. Monetization inconsistent. Visibility unreported. | Editor's marks | Ivory | Created | Print master done |
| 05 | My authentic self is currently being monetized. | Price tag | Brick | Created | Print master done |
| 06 | Sent 2:14 AM. Regretted 2:15 AM. | Giant times | True Navy | Created | Print master done |

- **Garment colors are locked to the real Comfort Colors names** (Ivory, True Navy, Brick). The site, cart, backend catalog and Printify products must all say the same color, and `scripts/check-apparel-manifest.py` fails the build if they don't. Brick is the closest available shade to the brand's oxblood and is **provisional until a physical sample is seen**.
- **Held back:** No. 07 Much Published, Little Said (the crest, saved for a later edition), No. 08 Order of the Blue Check, and Nos. 09 and 10. They stay in the manifest but are **not listed or built on the site**: the site shows only the six (`holidayLaunch: true`); to release another issue, set that flag and finish its Printify product, catalog entry and color. "I optimized this shirt for engagement" moved to No. 19.
- **Blank:** Comfort Colors 1717, provider Printify Choice, sizes S to 3XL, DTG print, front only.
- **Price:** $32 is a placeholder. The recommendation is **$36** with shipping at **$5.99 plus $2.49 per additional shirt**; awaiting Mark's decision.

## Calendar

Dates assume the real production and shipping time is what Printify's product pages suggest. **That is unverified** (the catalog API reports a 10-day handling time for every provider, which looks like a default), so a sample order is the only real test. The holiday cutoff has not been confirmed with the provider.

| When | Milestone | State |
|---|---|---|
| Nov 10 to 11 | Art approved, site and storefront built on `feature/holiday-six-storefront`, Printify drafts created, pricing analysis written | **Done** |
| Nov 11 to 13 | Merge to `develop`, deploy to dev, test orders on the six; staging after review | Next |
| Nov 12 to 20 | Legal and policy pages, shipping and returns, product copy, size chart, Printify mockups as interim images, email capture, social kit refreshed, tax and trademark questions raised | In progress; see launch-readiness |
| After everything above is ready | **Mark decides on samples** (four shirts is about $69) | Waiting on Mark |
| About 7 to 10 days after the sample order | Samples arrive; wash test; photograph on a person; approve or fix colors and art | Blocked on samples |
| Nov 27 to 30 | Soft launch window (Black Friday to Cyber Monday): live Stripe mode, one real order, refund, flip prod | **At risk**: needs samples ordered by about Nov 14 and every legal item done |
| Early December | Fallback launch if the sample step runs long | Fallback |
| About Dec 10 (to confirm) | Last-order-for-Christmas banner, once the provider's cutoff is known | Not set |

## What blocks launch (ranked)

1. **Samples.** They confirm the real Brick and True Navy colors, print quality on dark garments, the thin frame lines on textured cotton, and the true production time. Spends money, so Mark decides.
2. **Legal and policy pages.** Terms, Privacy, Cookies, Shipping and Returns are placeholders; live payments need them. Needs Mark's policy decisions and, ideally, counsel.
3. **Sales tax.** Whether we collect, whether Printify's tax can be avoided with a resale certificate, and whether to use Stripe Tax. Accountant.
4. **Trademark.** The brand name, tagline and the six sayings are not cleared. We can launch with a documented knockout search and the risk accepted, but the site must never claim clearance. Mark's call.
5. **Stripe live mode.** Not started. Needs the single-live-account decision, the live product catalog and Mark's explicit go.
6. **Real photos.** Samples on a person become the product images. Until then the site uses art on the real blank color.
7. **Prod flip.** `SHOW_COMING_SOON=false` plus promotion to `main`. Never without Mark's explicit go.

## Decisions needed from Mark

1. Price: $36 for all six (recommended), or $34 or $38.
2. Shipping: $5.99 plus $2.49 per extra shirt (recommended), or flat $5.99.
3. Returns and replacement policy (default proposed in launch-readiness).
4. Trademark: search-and-launch, or hold until counsel clears.
5. Launch window: Black Friday weekend, or early December with more polish.
6. Samples: when, and which four.

## Not in scope for the holiday launch

Back prints, sleeve seals, garment QR codes, hoodies, Nos. 07 to 10, the Wave 2 designs, the 12-month calendar drops, marketplace listings.

## Change log

| Date | Change |
|---|---|
| Nov 9, 2026 | First plan: five shirts (01, 02, 03, 05, 08) |
| Nov 10, 2026 | Approved six: 01 to 06 as above. 07 (crest) and 08 (Blue Check) dropped; "Sent" and the rewritten creator line added; numbering reset to 01 to 06; new artwork replaces the prototypes |
| Nov 11, 2026 (later) | Mark: show only the six issues. Nos. 07 to 10 removed from the shop, home page and product pages; the shop image is now a six-up sheet (`front-art-holiday-six.png`) and the Royal Commemorations collection is hidden |
| Nov 11, 2026 | Storefront rebuilt for the six; six Printify drafts created and the old test product deleted; garment colors locked to real blank names; shop-page concept studies removed; pricing analysis written (recommends $36); plan rewritten |
