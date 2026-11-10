# Founding collection print candidates

This folder contains six provider-neutral, transparent 4500 x 5400 PNG files prepared for garment-placement and physical sample review.

## Current gate

- Nos. 01-06 are **print candidates**, not production-approved products. They still require placement against the selected Printify garment template and a physical sample.
- Nos. 07-10 are intentionally absent. Their older sparse SVGs conflict with the approved ornate visual direction.
- Cleaned proofs of the selected ornate Nos. 07-10 artwork are in `production/qa/ornate-raster-upscales/` for composition review only. The export script also generates local 4500 x 5400 intermediates in that folder, but Git ignores them because their 1122 x 1402 source plates cannot become print masters through enlargement.

`MANIFEST.tsv` records dimensions, alpha support, proof garment color, and SHA-256 digest for each candidate.

Regenerate the package with:

```sh
./scripts/export-founding-ten-print-files.sh
```
