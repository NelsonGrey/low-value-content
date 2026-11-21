# Blank, provider and print specification

Status: updated November 11, 2026. The **Verified facts** section below supersedes the estimates in the rest of this page, which are kept as the original reasoning. Price and margin now live in [pricing-and-cost-analysis.md](pricing-and-cost-analysis.md). Nothing has been checked on a physical sample yet.

## Verified facts (Printify API, November 11, 2026)

| Item | Value |
|---|---|
| Blank | Comfort Colors 1717 garment-dyed tee (Printify blueprint 706): 6.1 oz pre-shrunk ring-spun cotton, relaxed fit, double-needle stitching, no side seams, sewn-in label, made in Honduras |
| Provider | Printify Choice (provider 99). Ten other providers carry the blank; Printful (410) and SwiftPOD (39) have the same three colors, with smaller print areas (3425 x 3882 and 3461 x 3955 px) |
| Colors we use | **Ivory**, **True Navy**, **Brick**, all in stock for S to 3XL. The catalog also has "Navy" (renders as a grey-blue) and "Crimson" (renders as a coral red), which we rejected. No Comfort Colors shade is called oxblood; Brick is the nearest we tested, so it is provisional until a sample |
| Sizes sold | S, M, L, XL, 2XL, 3XL (4XL exists on some colors; not used) |
| Print method | DTG. Front print area 3703 x 4200 px. Our 4500 x 5400 art is fitted to the height (scale 0.945), so it prints about 11.7 in wide and 14 in tall |
| Production cost | S to XL **$12.65**, 2XL $13.89, 3XL $16.03 |
| US shipping (Printify's quote) | $5.35 first shirt, $2.40 each additional shirt |
| Care | Machine wash cold (max 30 °C), do not bleach, tumble dry low, iron on low heat, do not dry clean |
| Handling time | The API reports 10 days for every provider, which looks like a default. Real production time is unverified |

**Print-quality flag.** At the scale Printify fits our art, the thinnest rule in each frame is about 0.029 in, just under our own 0.03 in minimum. The samples will show whether that holds on textured garment-dyed cotton.

**Interim mockups.** Printify renders mockups for every color we enabled. They are what the site can show until sample photography exists.

## Original reasoning (kept for reference)

## Recommended blank: Comfort Colors 1717 (garment-dyed)

Why it beats the main alternative, the Bella+Canvas 3001:

| | Comfort Colors 1717 | Bella+Canvas 3001 |
|---|---|---|
| Typical POD base cost | about $10-16 | about $8-13 |
| Retail sweet spot | $30-42 | $24-32 |
| Fabric and fit | 6.1 oz ring-spun, garment-dyed, relaxed and boxy | 4.2 oz, lighter, slim and tapered |
| Look | Soft, vintage, muted colours | Crisp, bright |
| Shrinkage | Minimal (garment-dyed) | Moderate |
| Fits our palette | Ivory is a standard colour; the garment-dyed look suits heraldic art | Natural, Maroon, Navy, Black exist |

Source figures: SellerMockups and Dropstudio blank comparisons and a July 2026 Printify cost breakdown (links in the sources list). They are a seller's blog ranges, not Printify's live prices.

**Why it is the more profitable choice for this brand.** The base cost is a few dollars higher, but the relaxed, garment-dyed look supports a higher price. At the planned $32:

- Comfort Colors at about $13 base leaves roughly $19 before fees and about $17.80 after Stripe's 2.9% + 30 cents.
- Bella+Canvas at about $10.50 base leaves roughly $21.50 before fees and about $20.30 after.

Bella+Canvas wins on margin at $32. Comfort Colors wins when the price rises: at $36 it leaves about $21.70 after fees, slightly more than Bella+Canvas at $32. The brand is positioned as official regalia in heraldic art, not a bargain graphic tee, so a $36 price on a heavier, soft-washed garment is believable. It also shrinks less, which means fewer fit complaints and returns. **Recommendation: Comfort Colors 1717 at $34-36, test one price against the other.** If you would rather compete on price, Bella+Canvas 3001 at $32 is the sound fallback.

The shipping line in the checkout currently charges a flat $5.99. That is typically at or above the first-item cost for a single tee, so it is not a profit lever either way.

## Printing method and the quality / printability balance

All Printify tees are printed DTG (direct to garment). Two kinds of artwork, two rules:

**1. The vector notices (Nos. 01-06 and all of Wave 2).** SVG source, rendered to a 4500 x 5400 px transparent PNG. Navy, oxblood, antique gold and ivory on four garment colours. Prints sharply at any size. Rules for every notice: no line thinner than about 0.03 in (the thinnest rule in the current frames is about that at a 12 in print, and DTG handles finer), no type smaller than about 0.2 in font size, and knockout (garment-colour) text such as "MONETIZED" is not a third ink.

**2. The heraldic plates (Nos. 07-10).** Full-colour artwork supplied at 1122 x 1402 px, which is about 94 dpi at a 12 in print. That is the gap between design quality and printability. The approach:

- Print at 12 x 15 in (3600 x 4500 px at 300 dpi), a standard chest print.
- Upscale with Real-ESRGAN x4plus, then blend 60% of that with 40% of a plain Lanczos resample of the original (`scripts/upscale-plates.py`). The AI pass gives crisp gold contours but adds painterly artefacts in fine texture such as moth fur; the plain resample is clean but soft. The blend keeps the edges and calms the texture.
- Plates keep their transparent backgrounds so the garment shows through. On dark garments Printify prints a white underbase behind the colours, which keeps gold and blue accurate.
- These are **candidate** print files. They must be sampled on the real garment before approval. If the fur and engraving detail looks soft or artefacted on the sample, the fallback is to redraw the plate as a simplified vector (a flat-colour engraving of the same composition), which prints perfectly but loses some of the painted richness. A commissioned redraw is the premium route.

Why not redraw all four now: the richness is the reason the plates exist, and a sample is cheap compared with a redraw. Test first.

## Verification checklist (first week)

1. In the Printify editor, open Comfort Colors 1717 and list the print providers: record base cost per colour and size, production time, and stock for Ivory, a burgundy/crimson shade, a navy, and Black.
2. Pick one provider and use it for the whole line (providers differ in colour range and size range).
3. Confirm the print area template (the front print width and height) and set the placement for the notices and plates.
4. Order samples of No. 01 (notice), No. 03 (notice on oxblood), No. 08 (plate on black) and No. 10 (plate on ivory). Wash test each.
5. Fill in the real colour names in the manifest and on product pages; record the real base costs here and in the business plan update.
6. Check what the existing test product (No. 01) is actually on: the catalog's note mentions an Ivory colour to enable, which fits Comfort Colors, but the blueprint and provider IDs are not stored in the repo.

## Sources

- [Bella Canvas 3001 vs Comfort Colors 1717: Which to Sell, SellerMockups](https://www.sellermockups.com/blog/bella-canvas-3001-vs-comfort-colors-1717)
- [Comfort Colors 1717 vs. Bella Canvas 3001: Which Should You Sell?, Dropstudio](https://dropstudio.io/blog/comfort-colors-1717-vs-bella-canvas-3001)
- [Printify Bella+Canvas 3001 base cost breakdown, PODVector, July 2026](https://podvector.ai/articles/printify/costs-and-charges/printify-bella-canvas-3001-base-cost-2025-full-breakdown-for-pod-sellers)
