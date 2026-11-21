#!/usr/bin/env python3
"""Unit economics for the Low Value Content holiday six.

    python3 tools/pricing/model.py            # prints every table used in docs/product/pricing-and-cost-analysis.md

Every input is in INPUTS below, tagged VERIFIED (read from the Printify/Stripe APIs or an
actual order on 2026-11-10/11) or ASSUMED (a planning guess to be replaced with data).
Change an input, re-run, and update the analysis document.
"""

INPUTS = {
    # --- VERIFIED: Printify, Comfort Colors 1717, provider Printify Choice (99), read from the product variants
    "base_cost": {"S": 12.65, "M": 12.65, "L": 12.65, "XL": 12.65, "2XL": 13.89, "3XL": 16.03},
    # --- VERIFIED: Printify's own US shipping quote for these products (orders/shipping.json, standard)
    "ship_first": 5.35,
    "ship_additional": 2.40,
    # --- VERIFIED: what we charge today (functions/src/catalog.ts)
    "ship_charged_flat": 5.99,
    # --- VERIFIED: Stripe US standard card pricing (stripe.com/pricing)
    "stripe_pct": 0.029,
    "stripe_fixed": 0.30,
    "dispute_fee": 15.00,
    # --- VERIFIED once: Printify charged $1.58 sales tax on a $12.65 shirt + $5.35 shipping to Chicago (8.75%)
    "printify_tax_rate_high": 0.0875,
    # --- ASSUMED planning figures
    "printify_tax_rate_blended": 0.045,   # many states and exemptions; unknown until a resale certificate is on file
    "refund_rate": 0.04,                  # share of orders refunded (plan threshold: returns+replacements under 5%)
    "dispute_rate": 0.005,                # share of orders disputed
    "reprint_rate": 0.02,                 # defects Printify does not cover (they normally reprint at no charge)
}

PRICES = [30, 32, 34, 36, 38, 40]
CAC = [0, 5, 10, 15]


def stripe_fee(total):
    return INPUTS["stripe_pct"] * total + INPUTS["stripe_fixed"]


def order(price, qty=1, size="L", ship_charged=None, tax_rate=0.0, cac=0.0, sizes=None):
    """Contribution for one order. ship_charged None = flat $5.99 per order."""
    sizes = sizes or [size] * qty
    ship_in = INPUTS["ship_charged_flat"] if ship_charged is None else ship_charged
    revenue = price * qty + ship_in
    base = sum(INPUTS["base_cost"][s] for s in sizes)
    ship_out = INPUTS["ship_first"] + INPUTS["ship_additional"] * (qty - 1)
    tax = tax_rate * (base + ship_out)
    fee = stripe_fee(revenue)
    refunds = INPUTS["refund_rate"] * (price * qty)            # refunded product price (fee is not returned)
    disputes = INPUTS["dispute_rate"] * INPUTS["dispute_fee"]
    reprints = INPUTS["reprint_rate"] * (base + ship_out)
    cost = base + ship_out + tax + fee + refunds + disputes + reprints
    return {"revenue": revenue, "base": base, "ship_out": ship_out, "tax": tax, "stripe": fee,
            "reserves": refunds + disputes + reprints, "total_cost": cost,
            "contribution": revenue - cost, "after_marketing": revenue - cost - cac * 1}


def main():
    i = INPUTS
    print("== Cost stack for ONE shirt, size L, flat $5.99 shipping charged, no tax paid, no reserves ==")
    print(f"{'price':>6} {'revenue':>8} {'base':>6} {'ship':>6} {'stripe':>7} {'margin':>7} {'margin %':>9}")
    for p in PRICES:
        rev = p + i["ship_charged_flat"]
        m = rev - i["base_cost"]["L"] - i["ship_first"] - stripe_fee(rev)
        print(f"{p:>6} {rev:>8.2f} {i['base_cost']['L']:>6.2f} {i['ship_first']:>6.2f} {stripe_fee(rev):>7.2f} {m:>7.2f} {m / rev * 100:>8.1f}%")

    print("\n== Contribution per single-shirt order (size L) after reserves, by price and marketing cost per order ==")
    for label, tr in (("Printify tax 0% (resale certificate)", 0.0), ("Printify tax 4.5% blended", i["printify_tax_rate_blended"]), ("Printify tax 8.75% (Chicago test)", i["printify_tax_rate_high"])):
        print(label)
        print(f"{'price':>6} " + " ".join(f"CAC${c:>3}".rjust(9) for c in CAC))
        for p in PRICES:
            o = order(p, tax_rate=tr)
            print(f"{p:>6} " + " ".join(f"{o['contribution'] - c:>9.2f}" for c in CAC))

    print("\n== Size effect at $36, single shirt, tax 4.5% ==")
    for s in ("S", "L", "2XL", "3XL"):
        o = order(36, size=s, tax_rate=i["printify_tax_rate_blended"])
        print(f"{s:>4}: base {i['base_cost'][s]:.2f}  contribution {o['contribution']:.2f}")

    print("\n== Multi-shirt orders at $36, tax 4.5%: flat $5.99 shipping vs $5.99 + $2.49 per extra shirt ==")
    print(f"{'qty':>4} {'flat':>8} {'tiered':>8}")
    for q in (1, 2, 3, 4, 6):
        flat = order(36, qty=q, tax_rate=i["printify_tax_rate_blended"])["contribution"]
        tier = order(36, qty=q, tax_rate=i["printify_tax_rate_blended"], ship_charged=5.99 + 2.49 * (q - 1))["contribution"]
        print(f"{q:>4} {flat:>8.2f} {tier:>8.2f}")

    print("\n== Break-even marketing cost per order (contribution before marketing) at tax 4.5% ==")
    for p in PRICES:
        print(f"${p}: {order(p, tax_rate=i['printify_tax_rate_blended'])['contribution']:.2f}")

    print("\n== Four-shirt sample order (one order, mixed sizes L) ==")
    base = 4 * i["base_cost"]["L"]
    ship = i["ship_first"] + 3 * i["ship_additional"]
    print(f"base {base:.2f} + shipping {ship:.2f} = {base + ship:.2f}; with tax 8.75% {(base + ship) * 1.0875:.2f}")


if __name__ == "__main__":
    main()
