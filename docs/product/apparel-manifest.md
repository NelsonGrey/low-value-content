# Master Apparel and Asset Manifest

The machine-readable source is [`apparel-manifest.json`](apparel-manifest.json). It preserves the original apparel work while connecting it to the Royal House of Engagement, the future storefront, QR experiences, Stripe checkout, and Printify fulfillment. The governing fiction and naming rules live in the [`Constitution of Engagement`](../brand/CONSTITUTION_OF_ENGAGEMENT.md).

The broader commercial-creative inventory is maintained in the [`Ecosystem Apparel Catalog`](ECOSYSTEM_APPAREL_CATALOG.md), with machine-readable classifications in [`ecosystem-apparel-catalog.json`](ecosystem-apparel-catalog.json). It reconciles the Founding Ten with the original 100-concept library and assigns each concept a printable issue form, ecosystem relationship, and imagery brief.

## What remains unchanged

- **Low Value Content** is the consumer brand.
- The original 100 sayings remain in [`concept-catalog.md`](concept-catalog.md).
- The original six editable SVG designs remain the foundation of the first release.
- Existing product IDs and commerce mappings are preserved.
- Stripe remains the checkout provider; Printify remains the production and fulfillment provider.

## What the House adds

**Low Value Content** is the portal, purveyor, owned domain, and maker's mark. **The Royal House of Engagement** is the ruling institution inside the fictional realm. It adds provenance, lineage, Great Houses, peerage, orders, Latin mottos, annual observances, commemorative editions, and QR experiences without requiring every shirt to use heraldic artwork.

The Crown governs the Attention Economy by converting attention into impressions, impressions into influence, and influence into evidence of importance. English carries the declaration; Latin supplies ceremonial texture and is always translated in public-facing copy.

## Ten-product launch matrix

| # | Product | Launch collection | Realm intensity | Creative status | Commerce status |
|---:|---|---|---|---|---|
| 1 | Please validate me algorithmically. | Public Notices | None | Editable SVG | Test sellable: White / L |
| 2 | Thought leader. No thoughts required. | Court & Orders | Moderate | Editable SVG | Planned |
| 3 | I’m not doomscrolling. I’m doing market research. | Court & Orders | Moderate | Editable SVG | Planned |
| 4 | Content creator. Meaning pending. | Public Notices | None | Editable SVG | Planned |
| 5 | My authentic self is currently being monetized. | Public Notices | None | Editable SVG | Planned |
| 6 | I optimized this shirt for engagement. | Public Notices | Light | Editable SVG | Planned |
| 7 | Much Published, Little Said | Court & Orders | Full | Ornate art plate | Planned |
| 8 | Order of the Blue Check | Court & Orders | Full | Ornate art plate | Planned |
| 9 | The End of the World Has Been Postponed | Royal Commemorations | Full | Ornate art plate | Planned |
| 10 | Patron Saint of Debugging | Royal Commemorations | Full | Ornate art plate | Planned |

The ten garments are one wardrobe with three degrees of ceremony. **Public Notices** are direct editorial observations and do not need a House. **Court & Orders** use appointments, institutions, medals, seals, or sovereign heraldry where those devices establish authority. **Royal Commemorations** use lineage and calendar history as the premise itself.

Every launch garment is front-only. The saying and artwork must succeed in one print area. Houses, offices, reigns, ceremonial titles, and QR stories begin on the website, hangtags, or packaging inserts; sleeve marks, back prints, and garment QR seals remain optional future premium treatments after physical testing. `LO I, the Interrupted` remains a strong future commemorative design rather than displacing an existing launch shirt.

## Status meanings

- **Editable prototype:** An existing SVG and rendered preview are present, but type, garment, placement, and print specifications still require production approval.
- **Concept mockup:** A generated presentation image exists, but production artwork does not.
- **Copy approved for development:** The concept and wording are selected for design exploration; there is no production artwork.
- **Planned:** The storefront may preview the concept but must not offer it for sale.
- **Test sellable:** A real Printify product and at least one variant are connected, but the purchase remains part of the test flow until sampling and launch approval are complete.

## Storefront contract

Every product page must combine two layers in proportion to the design:

1. Clear commercial information: actual photography, sizes, colors, price, fit, care, shipping, returns, and an honest availability state.
2. Optional fictional provenance: collection, Realm intensity, and—only when relevant—House, reign, Latin motto, proclamation, QR route, or ceremonial title.

The commercial layer always governs where ceremonial presentation conflicts with customer clarity. Prices and Printify IDs remain server-authoritative in `functions/src/catalog.ts`.

The exact `frontArtDisplay` image is the storefront authority for what will print. Older generated shirt scenes and front/back studies are retained as concept references, but they are not shown as alternate product artwork because they may contain details that are absent from the launch print file.

## Commerce ownership

- **Lowvaluecontent.com** owns product discovery, size and quantity selection, and any future multi-item cart.
- **Stripe Checkout** hosts the secure payment step after the site requests a server-validated Checkout Session.
- **Printify** receives a paid order from the backend and handles production and fulfillment; it does not own the customer-facing cart.

The current storefront is a direct-buy test flow, not a persistent shopping cart: one product selection is sent to Stripe Checkout. The backend can validate multiple order lines, but a multi-item cart interface has not yet been implemented or approved for launch.

The front-art status of all ten designs and their provider preflight gates are documented in [`realm-front-art-production-notes.md`](realm-front-art-production-notes.md).

## Validation

Run:

```sh
python3 scripts/check-apparel-manifest.py
```

The check confirms that the original catalog still contains 100 numbered sayings, the launch matrix contains ten unique products, declared assets exist, storefront product IDs appear in the manifest, and all sellable backend catalog entries have matching manifest commerce data.
