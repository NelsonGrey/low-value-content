# Master Apparel and Asset Manifest

The machine-readable source is [`apparel-manifest.json`](apparel-manifest.json). It preserves the original apparel work while connecting it to La Maison de Valebasse, the future storefront, QR experiences, Stripe checkout, and Printify fulfillment.

## What remains unchanged

- **Low Value Content** is the consumer brand.
- The original 100 sayings remain in [`concept-catalog.md`](concept-catalog.md).
- The original six editable SVG designs remain the foundation of the first release.
- Existing product IDs and commerce mappings are preserved.
- Stripe remains the checkout provider; Printify remains the production and fulfillment provider.

## What Valebasse adds

**Low Value Content** is the portal, purveyor, owned domain, and maker's mark. **La Maison de Valebasse** is the ruling dynasty inside the fictional realm. Valebasse adds provenance, lineage, houses, honors, Latin mottos, annual observances, commemorative editions, and QR experiences without requiring every shirt to use heraldic artwork.

The formal court style is **La Très Ancienne et Sérénissime Maison de Valebasse**. The apocryphal founder is **Count Lowvale of the Net**: `LOW VALUE CONTENT` can be rearranged exactly as `COUNT LOWVALE + NET`.

## Ten-product launch matrix

| # | Product | Treatment | Creative status | Commerce status |
|---:|---|---|---|---|
| 1 | Please validate me algorithmically. | Formal Petition for Algorithmic Recognition | Editable SVG | Test sellable: White / L |
| 2 | Thought leader. No thoughts required. | Official Court Appointment | Editable SVG | Planned |
| 3 | I’m not doomscrolling. I’m doing market research. | Royal Institute of Digital Inquiry | Editable SVG | Planned |
| 4 | Content creator. Meaning pending. | Unfinished Illuminated Proclamation | Editable SVG | Planned |
| 5 | My authentic self is currently being monetized. | Royal Portrait and Auction Inventory | Editable SVG | Planned |
| 6 | I optimized this shirt for engagement. | Office of Engagement Performance Report | Editable SVG | Planned |
| 7 | Much Published, Little Said | Full Peacock-and-Parrot Arms | Concept mockup | Planned |
| 8 | Order of the Blue Check | Medal for Distinguished Personal Visibility | Concept mockup | Planned |
| 9 | The End of the World Has Been Postponed | Y2K Millennium Interregnum | Copy ready for design | Planned |
| 10 | Patron Saint of Debugging | Feast of Saint Moth | Copy ready for design | Planned |

The ten garments are now one wardrobe rather than two adjacent concepts. Every shirt follows the same constitution: the original joke remains dominant on the front; a restrained House seal appears on the left sleeve; and the upper back carries the issuing office, reign, ceremonial title, and permanent QR route. The realm extends the joke without making the joke harder to read.

The first six retain their original editable artwork and gain Valebasse through placement and provenance. The final four use heraldry, honors, lineage, and calendar observances as the joke itself. `LO I, the Interrupted` remains a strong future commemorative design rather than displacing an existing launch shirt.

## Status meanings

- **Editable prototype:** An existing SVG and rendered preview are present, but type, garment, placement, and print specifications still require production approval.
- **Concept mockup:** A generated presentation image exists, but production artwork does not.
- **Copy approved for development:** The concept and wording are selected for design exploration; there is no production artwork.
- **Planned:** The storefront may preview the concept but must not offer it for sale.
- **Test sellable:** A real Printify product and at least one variant are connected, but the purchase remains part of the test flow until sampling and launch approval are complete.

## Storefront contract

Every product page must combine two layers:

1. Clear commercial information: actual photography, sizes, colors, price, fit, care, shipping, returns, and an honest availability state.
2. Fictional provenance: family, house, reign, Latin motto, proclamation, QR route, and ceremonial title.

The commercial layer always wins when clarity and satire conflict. Prices and Printify IDs remain server-authoritative in `functions/src/catalog.ts`.

## Validation

Run:

```sh
python3 scripts/check-apparel-manifest.py
```

The check confirms that the original catalog still contains 100 numbered sayings, the launch matrix contains ten unique products, declared assets exist, storefront product IDs appear in the manifest, and all sellable backend catalog entries have matching manifest commerce data.
