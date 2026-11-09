# Holiday 2026 launch plan: five shirts

Status: proposal, November 9, 2026. Nothing here is approved or ordered. Scope rule: launch small, prove the pipeline end to end, add Wave 2 in January.

## The five

| Order | No. | Design | Form | Why it is in |
|---:|---:|---|---|---|
| 1 | 01 | Please validate me algorithmically. | Vector notice | Already wired to Stripe + Printify (test mode). Fastest path, broadest joke. |
| 2 | 02 | Thought leader. No thoughts required. | Vector notice | Best gift shirt for the LinkedIn-adjacent crowd. |
| 3 | 03 | I'm not doomscrolling. I'm doing market research. | Vector notice | Most shareable line in the catalog; the circular seal photographs well. |
| 4 | 05 | My authentic self is currently being monetized. | Vector notice | Creator-economy hook; widens the audience beyond office workers. |
| 5 | 08 | Order of the Blue Check | Heraldic plate (hero) | The brand differentiator: the one piece that shows what the Realm is. |

Reserve, ready to add with no new art: 04 Content creator, 06 Optimized for engagement. Held for later: 07, 09, 10 (plates that need the same print-resolution work as 08), and all Wave 2.

Why only one plate: the four vector notices are print-ready from SVG. The plates need an upscale pass or redraw (see [blank-and-print-spec.md](blank-and-print-spec.md)) and a real sample before approval. One plate limits that risk to a single design. If the No. 08 sample looks soft, drop to four and the launch still stands.

## Calendar (working backwards)

Dates assume Printify production of about 2-5 business days plus US ground shipping. **The real holiday cutoff has not been checked**; confirm it with the chosen print provider in step 1 and move the dates accordingly.

| When | Milestone |
|---|---|
| Nov 9-12 | Pick blank + provider in the Printify editor (Comfort Colors 1717 recommended). Create the 5 products. Order samples of 01, 03 and 08 (the three that test different risks: simple notice, oxblood garment, plate on black). |
| Nov 10-20 | In parallel: print-resolution file for No. 08; trademark knockout searches; legal, shipping and returns pages; product copy (fit, fabric, care) from the real blank. |
| Nov 20-24 | Samples arrive. Wash test. Photograph on a person. Approve or fix. |
| Nov 25 | Stripe live mode on, one real test order end to end, then refund it. |
| Nov 27-30 | **Soft launch** (Black Friday weekend to Cyber Monday): flip prod. Email/waitlist and social go out. |
| About Dec 10 | Last-order-for-Christmas banner (set from the provider cutoff). |
| Dec 14 onward | Stop promising Christmas delivery; sell it as a gift certificate-style note or "arrives in January". |

## What blocks launch (ranked)

1. **Printify blank, provider and samples.** Critical path. Everything on the product page (fit, fabric, size chart, colors) depends on it. Needs your Printify account actions and about $60-100 in sample orders.
2. **Real photos.** Samples on a person are the product images. Flat art alone will not sell a $34 shirt.
3. **Legal and policy pages.** Terms, Privacy, Cookies, shipping and returns are placeholders today. Cannot take live payments without them.
4. **Trademark.** Brand name, tagline and the five sayings are not cleared. We can launch with a documented knockout search and the risk accepted, but the site must not claim clearance. Your call on risk tolerance.
5. **Stripe live mode and catalog.** `functions/src/catalog.ts` has one variant of one product. Needs all five products with the real size/color variant IDs, and a decision on shipping (flat $5.99 now).
6. **Prod flip.** `SHOW_COMING_SOON=false` plus promotion to `main`. Not done without your explicit go.
7. **Email capture and social accounts.** The social kit (profiles, 58 feed cards, schedule) exists. The accounts and a waitlist form do not.

## Decisions needed from Mark

1. Approve the five (or swap any).
2. Price test: $34 vs $36 on Comfort Colors, or fall back to Bella+Canvas 3001 at $32.
3. Go on Printify product creation and the sample order (spends money).
4. Trademark: search-and-launch, or hold until counsel clears?
5. Launch window: Black Friday weekend soft launch, or a week later with more polish?

## Not in scope

Back prints, QR garment seals, hoodies, Wave 2, the 12-month calendar drops, marketplace listings. All revisit in January.
