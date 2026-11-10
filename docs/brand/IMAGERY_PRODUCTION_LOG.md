# Imagery Production Log

This log records generated raster assets made under [`IMAGERY_DIRECTION.md`](IMAGERY_DIRECTION.md). It preserves the reference, prompt intent, review status, and production boundary for each image.

## 2026-10-19 — Tier 0 artwork plates, first pass

Status: **art-direction drafts**. These files are suitable for website concept presentation and for establishing the next garment-mockup pass. They are not production-ready Printify artwork: each file is 1122 × 1402 px, below the direction's 2400-pixel minimum and below a typical full-size 300-DPI garment-print target. Upscale-and-proof or redraw as production vectors before ordering samples.

All four files have transparent backgrounds and were generated with the built-in image-generation workflow. The existing Realm mannequin image named below was used as a visual reference; the model was instructed to extract only the chest artwork, remove the garment and room, preserve the composition, and reproduce the specified wording exactly.

| ID | Saved master | Reference | Prompt-specific direction | Review |
|---|---|---|---|---|
| A07 | `design/mockups/royal-house/A07-much-published-little-said.png` | `website/public/assets/shirt-07-realm.png` | Peacock and parrot supporters; navy shield; open book and sun; gold acanthus; exact banner “MUCH PUBLISHED, LITTLE SAID.” | Passes initial two-second and text checks. |
| A08 | `design/mockups/royal-house/A08-order-blue-check.png` | `website/public/assets/shirt-08-realm.png` | Blue-and-ivory ribbon; antique-gold starburst medal; generic ivory check; exact text “ORDER OF THE BLUE CHECK.” | Passes initial two-second and text checks; still requires rights review of the generic check device. |
| A09 | `design/mockups/royal-house/A09-y2k-postponed.png` | `website/public/assets/shirt-09-realm.png` | Crowned cartouche; split `99 | 00` clock; hourglass; crossed vintage cables; exact English and Latin banners. | Passes initial two-second and text checks. |
| A10 | `design/mockups/royal-house/A10-patron-saint-debugging.png` | `website/public/assets/shirt-10-realm.png` | Realistic moth; circuit halo; navy-and-gold ornament; recognizable vintage relay; exact English and Latin banners. | Passes initial two-second and text checks. |

### Shared generation direction

> Rich antique heraldic illustration in the manner of a finely engraved coat of arms, deep full colour, crisp screen-print-friendly edges, flat even lighting. Vertical 4:5 composition, centered, with generous transparent margin and nothing cropped. One isolated graphic only: no garment, mannequin, room, props, photographic scene, shadows, extra wording, watermark, modern logo styling, or cartoon treatment.

### Next review gates

1. Review the four compositions together for consistent line weight, gold treatment, banner scale, and visual authority.
2. Confirm A08 is sufficiently distinct from real-platform verification marks.
3. Decide whether A03 receives the proposed lion-and-loading-spinner redesign before generating it.
4. Produce print-resolution redraws or approved high-quality upscales, then order physical samples before treating any plate as production art.
5. Only after the plates are approved, use them as locked references for future P07–P10 garment images.

## 2026-10-31 — Plates adopted as storefront display art

The A07–A10 plates became the display art for Nos. 07–10 on the storefront and replaced the retired line art in the shop proof sheet. The site files `website/public/assets/front-art-07…10-*.png` are 720 × 900 palette-quantized derivatives of the plates, made for web delivery only. They are not print files, and the product pages label them "Artwork plate · not yet print-ready".
