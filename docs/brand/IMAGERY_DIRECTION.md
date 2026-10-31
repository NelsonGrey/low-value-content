# Imagery Direction

Status: working direction, drafted from the existing reference images. Extends [`HERALDIC_SYSTEM.md`](HERALDIC_SYSTEM.md), which still governs the marks themselves: **SVG files are canonical for the marks; raster images establish atmosphere, material, scale, and photography.** The one exception is Nos. 07–10, where the decision below makes the ornate raster plates the design source until print-resolution vector redraws exist. Nothing here overrides current names, copy, or product specifications in the master manifest.

The [`Ecosystem Apparel Catalog`](../product/ECOSYSTEM_APPAREL_CATALOG.md) applies this direction to the complete 104-product creative inventory. It determines whether a concept remains a typographic Public Notice or earns a House Warrant, Court & Order, or Royal Commemoration treatment before imagery is commissioned.

## References

| Image | What it establishes |
|---|---|
| `website/public/assets/royal-house/01-brand-identity-board.png` | The sovereign arms, seal, notification emblem, standard, on aged ivory paper |
| `.../02-apparel-collection.png` | The wardrobe on mannequins in the study, with folded stacks on marble |
| `.../03-ceremonial-packaging.png` | Box, tissue and wax seal, hangtag, membership card, standard, on a walnut desk |
| `website/public/assets/shirt-07-realm.png` to `shirt-10-realm.png` | The single-garment portrait shot (4:5, mannequin, panelled wall) |

The older flat `shirt-01.png` to `shirt-06.png` are legacy concept graphics and are **not** part of this direction.

## The visual DNA

Read the references as one world: **a private study in an old institution, photographed with total seriousness.** The joke is in the objects and the text. The photography never winks.

- **Setting:** warm greige plaster walls with carved pilaster panelling; dark turned-walnut furniture; tooled leather books; marble plinths and tabletops; a brass armillary sphere; an olive branch in a stone urn; dark wooden tailor's mannequin on a turned stand. These props repeat across images so the shots feel like one room.
- **Light:** soft diffused window light from camera left, warm amber fill, gentle vignette, no hard shadows, no flash.
- **Camera:** eye-level, slightly compressed (about 85mm), shallow depth of field. Garments are centered and fully visible. Portrait 4:5 for single products.
- **Palette:** navy, oxblood, antique gold, ivory, walnut brown. The blue of the Order of the Blue Check is the one sanctioned exception (`HERALDIC_SYSTEM.md`).
- **Materials:** heavyweight garment-dyed cotton, visible weave, soft print texture; gold foil on navy card; wax seal in oxblood; aged paper.
- **Ornament:** acanthus and laurel, scrolled banners, crowns. Heraldry is rich and exact, never cartoonish.
- **Tone:** over-serious luxury. No people, no hands, no smiling props, no meme imagery.

## Rules the canon already sets (follow them)

1. The peacock, parrot, notification shield, and Wi-Fi crown are reserved for the Crown and its highest warrants. **Do not put them on Public Notices.** Public Notices (Nos. 01, 04, 05, 06) stay typographic; the study surrounds them, the shirt does not gain heraldry.
2. Great House badges share one frame (crown, double rule, botanical supporters, shield, navy field, ivory face, gold line, oxblood charge) and differ only in the central charge.
3. Order insignia stay visibly subordinate to the sovereign arms.
4. Apparel and packaging images are **concept studies**, not Printify product photography. Caption them as such.
5. Slogans and the brand name are not trademark-cleared. Never imply they are.

## Style lock (prepend to every prompt)

> Photorealistic luxury still-life photograph in a private old-world study. Warm greige plaster walls with carved pilaster panelling, dark turned-walnut furniture, tooled leather books, marble surfaces, a brass armillary sphere, an olive branch in a stone urn. Soft diffused window light from the left with warm amber fill, gentle vignette, no hard shadows. Palette of navy, oxblood, antique gold, ivory, and walnut. 85mm lens, eye level, shallow depth of field, fine natural texture. Intentionally over-serious, museum-catalogue presentation. No people, no hands, no watermark, no logos or text other than what is specified, no extra decoration.

## Writing prompts that survive image models

- **Keep embedded text short and exact.** State it in quotes and say "this exact text, no other text." Anything longer than about eight words is likely to garble; plan to add long wording in the website instead.
- **Attach the artwork.** For any garment, attach the front-art file and say "reproduce this artwork exactly as a flat screen-print on the chest; do not redraw or embellish it."
- **Same room, same angle.** Reuse the style lock and say "same studio as the reference image," attaching `shirt-07-realm.png` as a layout reference.
- **Check the garment color** against the table below before accepting a result.
- Request **2400 px on the long edge** or larger so the site can make crisp smaller sizes.

## Decision: recognition beats minimalism

The jokes depend on the viewer recognising the object in a second or two. The current line-art front art for Court and Commemoration designs fails that test: the doves on No. 07 are shapeless, the moth on No. 10 reads as a flower or lightbulb, and the "99|00" clock on No. 09 reads as an open book. The mockups for 07 to 10 (peacock and parrot, painted moth, the "99:00" counter with crossed cables) are instantly legible.

**So the ornate, full-colour direction wins for the designs that rely on an image.** The line art for Nos. 07 to 10 is retired as a design source, and the mockups become the reference. Public Notices (01, 04, 05, 06) are typographic and already read at a glance, so they stay as they are.

Two things to confirm outside this repo:

- **Printing:** Printify is normally direct-to-garment and can print full colour, but ink limits, dark-garment underbase, and minimum resolution (print files are usually 300 DPI at the print size, e.g. 4500 x 5400 px) must be confirmed with the provider. AI-generated images are typically much smaller than that and will need a quality upscale or a vector redraw before production. This does not block the website.
- **No. 03:** the collection image shows an ornate "Duke of Doomscrolling" (lions around a shield with a loading spinner) that is clearly funnier than the current arc-and-arrow art. Decide whether No. 03 moves to that treatment.

## The legibility rule

Every image, product or not, must pass this before it ships:

1. **Two-second test.** Show it at about 200 px wide to someone who has not seen it. They should be able to say what the joke is, or at least name the central object (peacock, moth, medal, clock).
2. **One hero object**, centered, large, and made of familiar real-world icons (a heart badge, a cursor, a loading spinner, a blue check, a notification count).
3. **Text readable** at that size: three short lines at most.
4. If it needs a caption to be funny, it is not done.

## Garment colors (from `artSpecs` on the product pages)

| No. | Design | Garment | Inks / palette |
|---|---|---|---|
| 01 | Please validate me algorithmically. | Ivory | Navy + oxblood |
| 02 | Thought leader. No thoughts required. | Ivory | Archive navy + antique gold |
| 03 | I'm not doomscrolling. I'm doing market research. | Oxblood | Ivory + antique gold |
| 04 | Content creator. Meaning pending. | Ivory | Navy + oxblood |
| 05 | My authentic self is currently being monetized. | Ivory | Navy + oxblood |
| 06 | I optimized this shirt for engagement. | Ivory | Navy + oxblood |
| 07 | Much Published, Little Said | Navy | Ivory + antique gold |
| 08 | Order of the Blue Check | Black | Appointment blue + antique gold |
| 09 | The End of the World Has Been Postponed | Oxblood | Ivory + millennium gold |
| 10 | Patron Saint of Debugging | Ivory | Archive navy + antique gold |

## Shot list

Status: **Have** exists in the repo; **Need** must be generated. Aspect ratios are for the master image; the site derives smaller sizes.

### Tier 0: artwork plates (do these first)

The shirt art itself, generated alone, so mockups can reuse it exactly. Full colour, 4:5 portrait, centered, on a flat solid background (or transparent PNG if the tool supports it), 2400 px or larger, no garment and no scene. Same ornate heraldic style as the mockups. This is the print artwork, not a photograph, so **do not use the style lock**; use the one-line style below instead.

> Rich antique heraldic illustration in the manner of an engraved coat of arms, gold acanthus ornament, deep colour, crisp edges, flat even lighting, centered on a plain solid background, no scene, no shadows, no mockup.

| ID | Subject | Replaces | Status |
|---|---|---|---|
| A07 | The existing peacock-and-parrot arms with book-and-sun shield and banner, text "MUCH PUBLISHED, LITTLE SAID" (derive from `shirt-07-realm.png`) | `front-art-07` | Draft generated; see `IMAGERY_PRODUCTION_LOG.md` |
| A08 | Gold starburst medal with blue check, blue-and-ivory ribbon, text "ORDER OF THE BLUE CHECK" (from `shirt-08-realm.png`) | `front-art-08` | Draft generated; rights review remains |
| A09 | Crowned cartouche with split clock "99 | 00", hourglass, crossed computer cables, banner "THE END OF THE WORLD HAS BEEN POSTPONED" and "FINIS MUNDI DILATUS" (from `shirt-09-realm.png`) | `front-art-09` | Draft generated; see `IMAGERY_PRODUCTION_LOG.md` |
| A10 | Realistic moth with circuit-trace halo, laurels, vintage relay, banner "PATRON SAINT OF DEBUGGING" and "PRIMUS CASUS VERUS" (from `shirt-10-realm.png`) | `front-art-10` | Draft generated; see `IMAGERY_PRODUCTION_LOG.md` |
| A03 | (If approved) lions supporting a shield with a loading spinner and a crown, text "I'M NOT DOOMSCROLLING. I'M DOING MARKET RESEARCH." | `front-art-03` | Awaiting direction |

Attach the matching mockup as the reference and say: "Extract only the printed artwork from the shirt and redraw it flat on a plain background, keeping every element and every word."

### Tier 1: the product wardrobe (needed to launch)

Single garment, 4:5 portrait, the style lock plus the subject below. Attach the matching artwork plate (`A*`) where there is one, otherwise the current `front-art-*.png`.

| ID | Subject | Status |
|---|---|---|
| P01 | Warm-white heavyweight tee on the mannequin. Front print, exact text: "PLEASE VALIDATE ME ALGORITHMICALLY." Small red circular notification mark beneath. No heraldry. | Need |
| P02 | Warm-white tee. Navy and gold print: "THOUGHT LEADER." with the line "No thoughts required." and a small gold Wi-Fi-in-circle device above. | Need |
| P03 | Oxblood tee. Ivory and gold print: "I'm not doomscrolling." and "I'M DOING MARKET RESEARCH." inside concentric gold arcs with a downward arrow. | Need |
| P04 | Warm-white tee. Monospace black print: "CONTENT CREATOR. MEANING PENDING." above a black progress bar reading "PLEASE WAIT". No heraldry. | Need |
| P05 | Warm-white tee. Print: "MY AUTHENTIC SELF IS" above a red boxed "MONETIZED", then "CURRENTLY AVAILABLE". No heraldry. | Need |
| P06 | Warm-white tee. Print: "I OPTIMIZED THIS SHIRT FOR ENGAGEMENT." with a small chart rule beneath. No heraldry. | Need |
| P07 to P10 | Navy, washed-black, oxblood, ivory mannequin shots | Have. Keep; regenerate only if the A-plates change the art |

### Tier 2: the ceremonial system and page heroes

| ID | Subject | Aspect | Used on | Status |
|---|---|---|---|---|
| C01 | The founding identity plate | 3:2 | Home | Have |
| C02 | Collection on mannequins with folded stacks | 3:2 | Regalia | Have |
| C03 | Packaging and ceremonial materials flat lay | 4:3 | Regalia | Have |
| C04 | Hangtag close-up: cream card, gold peacock-and-parrot arms, "BY ALGORITHMIC APPOINTMENT" | 4:5 | Regalia, product pages | Need |
| C05 | Oxblood wax seal pressed on tissue, tissue printed with small gold crowned speech bubbles | 1:1 | Regalia | Need |
| C06 | Appointment card on a walnut desk beside a quill: "VISCOUNT OF VAGUEPOSTING" | 3:2 | Realm (peerage) | Need |
| C07 | The Royal Standard on a gilded pole, fringed, in the study | 4:5 | Realm | Need |
| H01 | Home hero: the sovereign arms carved and gilded above a study mantelpiece, candlelit | 16:9 | Home | Need |
| H02 | Realm hero: a long council table with six empty chairs, each with a different House badge on its back | 16:9 | Realm | Need |
| H03 | Lineage hero: a gallery wall of eleven small oval portrait frames in a row | 16:9 | Lineage | Need |
| H04 | Calendar hero: an open perpetual desk almanac with a ribbon marker and a wax-sealed date | 16:9 | Calendar | Need |
| H05 | Regalia hero: a tailor's atelier, folded garments on shelves, boxed tissue, a brass measuring tape | 16:9 | Regalia | Need |

### Tier 3: the full world (the Great Houses and the Lineage)

Still-life objects with the House badge as a small engraved or enamel plaque. One per subject, 4:5, same room.

| ID | Subject | Used on |
|---|---|---|
| G01 | House of Prompt: a brass writing instrument and blank parchment, a quill poised, a single cursor-like bar of gold ink | Realm |
| G02 | House of Scroll: an endless parchment roll cascading off a marble plinth to the floor | Realm |
| G03 | House of Influence: a gilt faceted star under a single spotlight, a hand mirror behind it | Realm |
| G04 | House of Signal: a brass pressure gauge and a chart with a gold ascending trace | Realm |
| G05 | House of Spam: identical sealed envelopes spilling from a leather post-bag | Realm |
| G06 | House of Buffer: an hourglass with a half-drawn gold ring, sand mid-fall | Realm |
| L01 | Moth I: a pinned moth specimen under glass beside a small brass relay | Lineage |
| L02 | LO I: a brass-and-glass terminal showing the two letters "LO" | Lineage |
| L03 | Spam I: a pile of identical envelopes, as G05 but a portrait frame | Lineage |
| L04 | Emoticon I: a gilt oval miniature of a sideways smile in a portrait frame | Lineage |
| L05 | Web I: a globe wrapped in gold thread on a stand | Lineage |
| L06 | Y2K, the Almost: a stopped clock reading 99:00 with a wax "disputed" seal | Lineage |
| L07 | Content I: a gilded folding camera and film reel | Lineage |
| L08 | Scroll I: as G02, cropped as a portrait | Lineage |
| L09 | Algorithm I: a veiled brass orrery, no face visible, a black cloth draped over it | Lineage |
| L10 | Prompt I: an ornate typewriter with an endless paper ribbon spilling off the platen | Lineage |
| U01 | 404: an empty gilded picture frame on a panelled wall, a small brass plaque left blank | 404 |
| U02 | Order status: a wax-sealed ledger on the desk | Order |

## What I will build when images arrive

1. Convert masters to AVIF and WebP at three widths, with an `<img>` that has correct dimensions and lazy loading (the current mockups are 2 to 3 MB PNGs).
2. Add an images manifest (file, alt text, caption, "concept study" flag) and one reusable component with a consistent gold-frame treatment.
3. Place each image per the tables above and set the manifest's `conceptMockup` and `conceptReference` fields so product pages pick them up automatically.
4. Review each image against this document and the product before it ships.

## Delivery and naming

- File name: `ID-slug.png`, for example `P03-doomscrolling-mannequin.png`. Put masters in `design/mockups/royal-house/`.
- 2400 px or larger on the long edge. No watermark.
- Tell me which prompt and any reference image you used, so a failed shot can be rerun.

## Acceptance checklist

- [ ] Same room, light, and camera as the references.
- [ ] Garment color matches the table.
- [ ] Printed text matches the manifest's text exactly, with no stray letters.
- [ ] The artwork matches the attached artwork plate exactly.
- [ ] Passes the two-second test (see the legibility rule).
- [ ] Public Notices carry no heraldry.
- [ ] No people, brand logos, or watermarks.
- [ ] The Blue Check device does not copy a real platform's mark closely enough to invite a rights question. Flag for review.
