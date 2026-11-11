# Pricing and cost analysis: the holiday six

Status: recommendation for Mark's decision, November 11, 2026. Nothing here has been approved. All figures come from `tools/pricing/model.py`; change an input there, re-run it, and update this page.

**Recommendation in one line:** price all six shirts at **$36**, charge shipping as **$5.99 for the first shirt plus $2.49 for each additional shirt**, and treat sales-tax handling as the one open item that could move the margin.

## 1. What is verified and what is assumed

| Input | Value | Basis |
|---|---|---|
| Blank and provider | Comfort Colors 1717, Printify Choice (provider 99) | Printify catalog API |
| Production cost, S to XL | **$12.65** | Read from our six Printify products on November 11 |
| Production cost, 2XL / 3XL | $13.89 / $16.03 | Same |
| Printify US shipping, first shirt | **$5.35** | Printify's own quote for these products (`orders/shipping.json`, standard) |
| Printify US shipping, each additional shirt | **$2.40** | Same (1 shirt $5.35, 2 shirts $7.75, 3 shirts $10.15, 6 shirts $17.35) |
| Shipping we charge today | $5.99 flat per order | `functions/src/catalog.ts` |
| Stripe fee | 2.9% + $0.30 per card payment, fee not returned on refund, $15 per dispute | [Stripe pricing](https://stripe.com/pricing) (confirm before launch; some cached pages were dated) |
| Printify sales tax | **$1.58** on one shirt plus shipping to Chicago (8.75% of $18.00) | One real test order, November 10 |
| Refund rate | 4% | Assumed. The brand plan's ceiling for returns plus replacements is 5% |
| Dispute rate | 0.5% | Assumed |
| Defects we pay for | 2% of cost | Assumed. Printify normally reprints misprints and damage at no charge |
| Other Printify tax outside Illinois | 0% to 8.75%; modelled at 4.5% blended | Assumed until we hold a resale certificate |

**Correction.** Earlier I quoted the production cost as about $16 per shirt. That was the 3XL price, the first variant I sampled. The cost for S to XL, which is nearly all sales, is **$12.65**.

**Cross-check on production cost:** [Printful lists](https://www.printful.com/custom/mens/shirts/unisex-garment-dyed-heavyweight-shirt-comfort-colors-1717) the same blank with one print from $15.60, so $12.65 through Printify Choice is a competitive base. Other print-on-demand sites list $16 to $20 ([Merchloop](https://merchloop.com/products/comfort-colors-1717), [NinjaPOD](https://ninjaprintondemand.com/products/unisex-garment-dyed-t-shirt)).

## 2. The cost stack for one shirt

Size L, flat $5.99 shipping charged, no tax and no reserves yet.

| Shirt price | Customer pays | Production | Printify shipping | Stripe | Margin | Margin % |
|---:|---:|---:|---:|---:|---:|---:|
| $30 | $35.99 | $12.65 | $5.35 | $1.34 | $16.65 | 46.3% |
| $32 | $37.99 | $12.65 | $5.35 | $1.40 | $18.59 | 48.9% |
| $34 | $39.99 | $12.65 | $5.35 | $1.46 | $20.53 | 51.3% |
| **$36** | **$41.99** | $12.65 | $5.35 | $1.52 | **$22.47** | 53.5% |
| $38 | $43.99 | $12.65 | $5.35 | $1.58 | $24.41 | 55.5% |
| $40 | $45.99 | $12.65 | $5.35 | $1.63 | $26.36 | 57.3% |

The $5.99 shipping we collect is almost exactly what Printify charges us ($5.35), so shipping is close to break-even on a single shirt and the shirt price carries the margin.

## 3. Contribution after reserves and marketing

Contribution = what is left of one single-shirt order after production, shipping, Stripe, Printify tax, expected refunds, disputes and defects, minus the cost of acquiring the customer. The brand plan's own thresholds are acquisition cost under **$10** and contribution after marketing of **$8 to $10** per shirt.

Printify tax at the 4.5% blended assumption:

| Price | Before marketing | Marketing $5 | **Marketing $10** | Marketing $15 |
|---:|---:|---:|---:|---:|
| $30 | $14.20 | $9.20 | $4.20 | -$0.80 |
| $32 | $16.06 | $11.06 | $6.06 | $1.06 |
| $34 | $17.93 | $12.93 | $7.93 | $2.93 |
| **$36** | **$19.79** | $14.79 | **$9.79** | $4.79 |
| $38 | $21.65 | $16.65 | $11.65 | $6.65 |
| $40 | $23.51 | $18.51 | $13.51 | $8.51 |

- **$32 does not meet the plan.** At $10 per customer it leaves $6.06.
- **$34 just misses.** $7.93 at $10, so it works only if acquisition costs under about $8.
- **$36 is the lowest price that meets the plan** ($9.79 at $10 per customer).
- **$38 adds comfort** and the most headroom if marketing costs more than planned.

Sensitivity to the Printify tax assumption (price $36, marketing $10): 0% tax gives $10.60, 4.5% gives $9.79, 8.75% (every order taxed like the Chicago test) gives $9.02. The tax question is worth less than $1.60 per order, so it matters but doesn't change the recommendation.

## 4. Sizes

Price is per design, not per size (the backend supports one price per product), so larger sizes cost more but sell for the same price.

| Size | Production | Contribution at $36 (before marketing) |
|---|---:|---:|
| S to XL | $12.65 | $19.79 |
| 2XL | $13.89 | $18.47 |
| 3XL | $16.03 | $16.19 |

Even 3XL is profitable, so keep all six sizes at one price. A size surcharge would be cleaner but needs a backend change we don't need yet.

## 5. Multi-shirt orders and shipping

Printify charges $5.35 for the first shirt and **$2.40 for each additional shirt**. A flat $5.99 per order loses money on shipping as the basket grows (three shirts cost us $10.15 and we collect $5.99). Tiered shipping of $5.99 plus $2.49 per extra shirt matches the real cost:

| Shirts in the order | Contribution with flat $5.99 | With $5.99 + $2.49 each extra |
|---:|---:|---:|
| 1 | $19.79 | $19.79 |
| 2 | $37.28 | $39.69 |
| 3 | $54.76 | $59.60 |
| 4 | $72.25 | $79.50 |
| 6 | $107.23 | $119.31 |

Tiered shipping is worth about $2.40 more per extra shirt, it is honest ("shipping scales with what you order") and it removes the incentive to feel punished for buying a second shirt. It needs a small change to `functions/src/checkout.ts` and the cart copy, which I'll make once you approve it.

A free-shipping threshold, for example free over two shirts, would cost $7.75 on a two-shirt order and lower the margin. I'd leave that out for launch.

## 6. Sales tax (the open item)

- **We charge customers no sales tax today** (`STRIPE_AUTOMATIC_TAX=false`). Whether we must collect depends on where we have nexus (economic thresholds by state, and our physical presence). That needs the accountant before live mode, and it can change the price the customer sees by up to 9%.
- **Printify charged us tax** ($1.58) on the test order. A reseller can usually avoid that by giving Printify a resale certificate. Check this with the accountant at the same time.
- **Stripe Tax** exists and charges an extra fee per transaction. Decide it with the accountant, because it only makes sense once we know where we owe tax.

## 7. Costs not in the per-shirt model

Not quantified yet; fill these in and add them to the model before launch:

| Cost | Status |
|---|---|
| Samples: four shirts in one order are about **$68.68** with tax ($50.60 production plus $12.55 shipping, taxed at the Chicago rate) | Computed |
| Printify Premium plan (a monthly fee for a discount on production cost). If the discount is around 20% it saves about $2.53 per shirt and pays for itself at modest volume | **Unverified: check the current price and discount** |
| Firebase Blaze usage (hosting, functions, Firestore) | Expected to be a few dollars a month at this volume; not measured |
| Domain, Google Workspace, email | Existing |
| Photography, trademark searches or counsel | Not budgeted |
| Marketing spend | Plan threshold is under $10 per customer |

## 8. Pricing position

I could not find direct comparables for satirical graphic tees. The only data I got were mainstream retail: [Levi's](https://www.levi.com/US/en_US/clothing/men/shirts/classic-graphic-tee/p/224910380) lists graphic tees at $28 to $40, and J.Crew Factory graphic tees list at up to $54.50. A premium garment-dyed blank with a collectible, numbered design supports $36 to $38. A competitor scan on Etsy, Threadless and Cotton Bureau would firm this up and is worth an hour of your time, because I can't reach those shops from here.

## 9. Decisions requested

1. **Price:** $36 for all six (recommended), or $34 / $38?
2. **Shipping:** $5.99 plus $2.49 per additional shirt (recommended), or keep flat $5.99?
3. **Sizes:** S to 3XL at one price (recommended), or S to 2XL only?
4. **Tax:** ask the accountant about collection, Printify's tax, and a resale certificate before live mode.

When 1 and 2 are decided I'll update `functions/src/catalog.ts`, the Printify product prices, the manifest and the cart copy together.
