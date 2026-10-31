# Launch Front-Art Production Notes

## Status

Nos. 01–06 have editable, transparent, 4500 × 5400 SVG masters and 750 × 900 PNG review renders. Nos. 07–10 follow the **ornate full-colour direction** chosen in [`IMAGERY_DIRECTION.md`](../brand/IMAGERY_DIRECTION.md): their earlier line-art SVGs are retired (kept in the manifest as `legacyArtwork`), and the selected artwork is the A07–A10 plates in `design/mockups/royal-house/`. Those plates are 1122 × 1402 px, so they are **working plates, not print files**; each needs a vector redraw or an approved upscale to print resolution. All ten are **print-oriented prototypes**, not files approved for fulfillment. Before upload, the selected Printify provider template must determine final physical dimensions, placement, color handling, and raster export settings. Live type in the SVG masters must be converted to outlines in the final vendor file.

## Shared construction

- One centered front print; no sleeve or back location.
- Nos. 01–06: two printed colors per design. Garment-color knockouts are not additional ink.
- Nos. 07–10: full colour. Ink limits, dark-garment underbase, and minimum resolution must be confirmed with the provider.
- Minimum principal stroke in the Nos. 01–06 SVG masters: approximately 20–44 source pixels before provider scaling.
- Transparent background.
- English joke remains dominant; Latin and dates remain subordinate.
- No QR code in launch artwork.
- The atmospheric storefront mockups remain concept references and are not print files.

## Issue specifications

| No. | Master | Garment direction | Printed colors | Garment-color role | Composition |
|---:|---|---|---|---|---|
| 01 | `design/prototypes/01-validate-me.svg` | Warm white | Editorial black `#171713`; notification red `#D9483B` | White remains visible through the loading and status composition | Request headline, incomplete loading loop, pending status |
| 02 | `design/prototypes/02-thought-leader.svg` | Warm white | Archive navy `#142B40`; antique gold `#BD9143` | White keeps the appointment seal and typography open | Direct joke with one restrained algorithmic appointment seal |
| 03 | `design/prototypes/03-market-research.svg` | Oxblood | Warm ivory `#E7D9BA`; antique gold `#C99B43` | Oxblood remains visible through the interrupted institute rings | Research-institute arches, clear type field, original joke, House of Scroll endorsement |
| 04 | `design/prototypes/04-content-creator.svg` | Warm white | Editorial black `#171713`; status red `#D9483B` | White status text is a garment-color knockout | Typewriter draft, unfinished status block, pending meaning |
| 05 | `design/prototypes/05-authentic-self.svg` | Warm white | Editorial black `#171713`; status red `#D9483B` | White `MONETIZED` lettering is a garment-color knockout | Transactional listing and monetization stamp |
| 06 | `design/prototypes/06-optimized-shirt.svg` | Warm white | Editorial black `#171713`; status red `#D9483B` | White remains the open report field | Experiment heading, result line, statistically insignificant chart |
| 07 | `design/mockups/royal-house/A07-much-published-little-said.png` | Deep navy | Full colour: peacock, macaw, navy shield, gold acanthus | Navy remains the field behind the shield and banner | Sovereign notification shield with peacock and parrot supporters, open book and sun, banner motto |
| 08 | `design/mockups/royal-house/A08-order-blue-check.png` | Washed black | Full colour: blue-and-ivory ribbon, gold starburst medal | Black remains the field behind the medal | Ribbon, starburst medal, generic check device, order title |
| 09 | `design/mockups/royal-house/A09-y2k-postponed.png` | Oxblood | Full colour: crown, `99 | 00` flip clock, hourglass, crossed cables, gold ornament | Oxblood remains the field behind the cartouche | Crowned cartouche, split clock, hourglass, crossed vintage cables, English and Latin banners |
| 10 | `design/mockups/royal-house/A10-patron-saint-debugging.png` | Warm ivory | Full colour: natural-history moth, gold circuit halo, navy ornament | Ivory remains the field behind the moth | Realistic moth, circuit halo, vintage relay, English and Latin banners |

## Preflight gates

Nos. 07–10 first need print-resolution artwork (vector redraw or approved upscale to 4500 × 5400 from the A07–A10 plates). Gates 3–4 below then apply to the Nos. 01–06 SVG masters; for Nos. 07–10 replace them with provider ink-limit and underbase review.

1. Select the launch blank and Printify print provider.
2. Place each master on that provider’s exact template at the intended physical width.
3. Convert all live text to vector outlines while retaining a separate editable source copy.
4. For Nos. 01–06, convert the two printed colors to named spot-color layers.
5. Inspect minimum strokes, counters, trapping, and registration at actual size.
6. Export provider-ready transparent PNGs at the provider’s required resolution and color profile.
7. Order one sample per garment/color combination.
8. Inspect registration, line retention, opacity, hand feel, placement, and small-type legibility.
9. Wash-test before enabling checkout.

No design should be labeled production-ready merely because its SVG and PNG render correctly on screen.
