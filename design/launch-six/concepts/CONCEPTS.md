# Low Value Content — holiday six, concept comps (round 1)

Rough review comps, 3 ideas per shirt. Not print-ready. Front only. Every file uses the shared
double-rule frame with diamond corners and the small imprint `THE ROYAL HOUSE OF ENGAGEMENT · NO. NN`.
All type is outlined from the approved fonts (Inter, Barlow Condensed ExtraBold, Libre Baskerville).
Each SVG is 4500×5400 with a transparent background and only its two inks. Comps are 1800×2160 on flat garment colour.

## No. 01 — Please validate me algorithmically. (ivory garment; navy + oxblood)
- **A · progress-bar** — Request-form notice; the hero is a wide navy progress track with a ~10% oxblood fill that never gets further.
- **B · queue-ticket** — Now-serving ticket: a huge navy `0001` under `PUBLIC REQUEST`, an oxblood perforation with notched ticket edges, then the plea and wait status.
- **C · pending-stamp** — Formal serif notice with a big oxblood rounded-rect `REQUEST / PENDING` status stamp, tilted 2°.

## No. 02 — Thought leader. No thoughts required. (navy garment; ivory + gold)
- **A · door-plaque** — Brass office plaque: a gold double-rule plate with corner screws, `THOUGHT / LEADER.` filling it in condensed ivory, and the italic disclaimer inside.
- **B · empty-thought** — Appointment diploma whose only device is a double gold ring with nothing in it (the missing thought), above a full-width `THOUGHT LEADER.`
- **C · influence-medal** — A single geometric order medal (rings, radiant ticks, faceted eight-point star), with `THOUGHT LEADER.` set as a band between double gold rules.

## No. 03 — I'm not doomscrolling. I'm doing market research. (oxblood garment; ivory + gold)
- **A · proceedings-cover** — Institute journal title page: a double-ruled masthead, the italic denial as an epigraph, a large three-line serif title, a Scroll feed-and-arrow journal mark, and the issue line.
- **B · inquiry-aperture** — A survey-reticle aperture (gold outer ring, ivory inner ring, four cardinal ticks) with the type set openly in the centre and a small Scroll mark below. No masked type band.
- **C · field-dispatch** — Field briefing: a tabbed header bar, the italic denial, a small `I'M DOING` lead-in, then a huge left-aligned condensed `MARKET / RESEARCH.`, and the footer with a small Scroll mark.

## No. 04 — Content creator. (ivory garment; navy + oxblood)
- **A · audit-ledger** — Centred editorial ledger: heavy `CONTENT CREATOR.`, three ruled Baskerville verdict rows, each with its own oxblood flag (hollow circle / half-filled / dotted circle).
- **B · editors-marks** — Manuscript returned with comments: a large serif title with `CREATOR.` looped in oxblood, and the three verdicts as staggered italic margin notes, each with an abstract proof mark (caret, double stroke, open loop).
- **C · scorecard** — Left-aligned inspection report card: a header rule, three ruled rows, and a boxed grade cell for each (empty / half-filled / dotted). No category headers.

## No. 05 — My authentic self is currently being monetized. (oxblood garment; ivory + gold)
- **A · price-tag** — A gold chamfered price tag with a transparent string hole and a short gold string rule. `MONETIZED` is knocked out of the tag, the item name sits above, and the fine print is below.
- **B · auction-plate** — Catalogue lot card: a wide gold hammer-price plate with a knocked-out serif `MONETIZED` and a knocked-out engraved inner border, then the conditions of sale under a double rule.
- **C · classified** — Newspaper-column listing: the sentence `MY AUTHENTIC SELF IS / [gold paid-highlight plate] / CURRENTLY AVAILABLE`, with the terms as fine print between column rules.

## No. 06 — Sent 2:14 AM. Regretted 2:15 AM. (navy garment; ivory + gold)
- **A · giant-times** — Huge ivory `2:14` over huge gold `2:15`, with `SENT`, `REGRETTED` and `AM.` as small labels. The status chain is small at the bottom, with a tiny Signal mark.
- **B · status-chain** — The four-beat chain stacked large in condensed type, with `REGRETTED` larger and in gold. The timestamp record is a ruled row underneath.
- **C · timeline** — A quiet left-aligned log: a gold spine with minute ticks, an ivory tick at `SENT 2:14 AM.` and a gold tick at `REGRETTED` / `2:15 AM.`, the chain below and the Signal mark at top left.

## Wording / ink confirmation
- An automated proof ran over every outlined string in every SVG (`check/proof.json`). In all 18 files, every required line appears exactly and no word outside the brief appears. The apostrophe in `I'm` / `I'M` is ASCII U+0027, with no curly quotes.
- Splits are line breaks or type-size changes only, with no rewording: `PUBLIC REQUEST` + `0001` (01-B), `REQUEST` / `PENDING` (01-C), `THOUGHT` / `LEADER.`, `MARKET` / `RESEARCH.`, `CONTENT` / `CREATOR.`, `SENT` `2:14` `AM.` (06-A), and the chain wrapped after each `·` (06-B). In 06-B, `REGRETTED` and `2:15 AM.` share one record line.
- Inks per file: 01 and 04 use only #142B40 and #852E34. 02, 03, 05 and 06 use only #E7D9BA and #C99B43. There is no third ink, and no crowns, heraldry, Latin, Wi-Fi or notification marks, chat bubbles, or Courier.
- No. 06 imprint reads `NO. 06`, and the saying is SENT. The Signal mark is measured bars plus an ascending trace.
- No. 05 knockouts are real geometry: the gold block minus the glyph outlines (skia-pathops boolean difference), with no SVG mask. Verification (`check/knockout.json`): rendering each SVG at 4500×5400 gives 100% alpha = 0 in the glyph interiors. That is 353,386 / 216,998 / 454,170 px for A / B / C, and the gold around the letters is solid. The side margins between the letters and the block are about 285 / 385 / 310 px.
- One change from build.py: the imprint letter-spacing is 16 instead of 26. At 80 / 26 the line ran into the diamond ornaments at x = 700 and 3800.
