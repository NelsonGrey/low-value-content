# Low Value Content — holiday launch six: print artwork

Mark's mixed picks, finished for print on November 10, 2026. Wording matches `docs/product/launch-six-art-brief.md`, except No. 05, which uses Mark's wording correction (the brief had copied earlier art). The earlier all-C print set is in `archive-all-c/`. Concept comps for all 18 directions are in `concepts/`. The first typographic pass is in `archive-first-pass/`.

The outlined SVG in `print/` is the authoritative file for each shirt.

| No. | Name | Concept | Garment | Inks (only) | Frame / imprint |
|---|---|---|---|---|---|
| 01 | Progress bar | 01-A | Ivory #F4EEDF | Navy #142B40 + Oxblood #852E34 | Oxblood, NO. 01 |
| 02 | Door plaque | 02-A | Navy #142B40 | Ivory #E7D9BA + Gold #C99B43 | Gold, NO. 02 |
| 03 | Field dispatch | 03-C | Oxblood #852E34 | Ivory #E7D9BA + Gold #C99B43 | Gold, NO. 03 |
| 04 | Editor's marks | 04-B | Ivory #F4EEDF | Navy #142B40 + Oxblood #852E34 | Oxblood, NO. 04 |
| 05 | Price tag | 05-A | Oxblood #852E34 | Ivory #E7D9BA + Gold #C99B43 | Gold, NO. 05 |
| 06 | Giant times | 06-A | Navy #142B40 | Ivory #E7D9BA + Gold #C99B43 | Gold, NO. 06 |

## Wording (letter for letter)
- **01:** PUBLIC REQUEST 0001 / PLEASE VALIDATE ME ALGORITHMICALLY. / REQUEST PENDING / ESTIMATED RECOGNITION · INDEFINITE
- **02:** BY ALGORITHMIC APPOINTMENT / THOUGHT LEADER. / No thoughts required. / OFFICIAL COURT APPOINTMENT · HONORARY
- **03:** ROYAL INSTITUTE OF DIGITAL INQUIRY / I'm not doomscrolling. / I'M DOING / MARKET RESEARCH. / HOUSE OF SCROLL · FIELD WORK CONTINUES
- **04:** CONTENT CREATOR. / Uniqueness questionable. / Monetization inconsistent. / Visibility unreported.
- **05** (Mark's correction):
  - Above the tag: MY AUTHENTIC SELF IS CURRENTLY BEING
  - Knocked out of the tag: MONETIZED
  - Fine print below: SPONSORSHIP SUBJECT TO TERMS / PERSONA MAY DIFFER FROM PERSON
  - "CURRENTLY AVAILABLE" is dropped.
- **06:** SENT 2:14 AM. / REGRETTED / 2:15 AM. / SENT · DELIVERED · READ · REGRETTED

Line breaks only, no rewording: THOUGHT / LEADER., MARKET / RESEARCH., CONTENT / CREATOR., HOUSE OF SCROLL · / FIELD WORK CONTINUES, MY AUTHENTIC SELF IS / CURRENTLY BEING, and SENT + 2:14 + AM. All apostrophes are plain ASCII.

## Files
- `editable/NN-slug.svg` — live type. Install the fonts in `fonts/` before opening. The 05 knockout stays an outlined compound path, with a hidden live `MONETIZED` text beside it. Renderers that substitute system fonts may show slightly different weights.
- `print/NN-slug.svg` — all type outlined. **This is the authoritative print master.**
- `print/NN-slug.png` — 4500×5400 RGBA, 300 dpi, embedded sRGB profile, rendered from the print SVG. Edges are hard: alpha is 0 or 255 only, and every opaque pixel is one of the two inks. If a printer prefers anti-aliased edges, re-render the print SVG directly.
- `previews/NN-slug.png` — flat garment-colour previews. `previews/launch-six-contact-sheet.png` shows all six.
- `fonts/` — Inter Regular / Medium / ExtraBold / Black, Libre Baskerville Regular / Bold / Italic, Barlow Condensed ExtraBold.
- `check/proof.json`, `check/knockout.json`, and 100% crops are included for reference.

## Print rules
- **Minimum sizes:** the thinnest line is 11 px (the inner frame rule); all artwork strokes are 12 px or more. The smallest type is the imprint, with a 72.4 px cap height.
- **Imprint:** Libre Baskerville, 94 px, 9 px tracking. It clears the corner diamonds by 88–97 px.
- **Placement:** all content sits inside the inner frame, above the imprint, and clear of the outer 3%.
- **05 knockout:** the gold tag, minus the string hole, minus the `MONETIZED` letter outlines, cut as a path boolean. There is no SVG mask. The oxblood garment shows through the letters and the hole.
