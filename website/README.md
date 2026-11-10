# Website

One Astro project: `src/` (pages, layout, components, data), `public/` (static assets, including the non-prod access gate), and `coming-soon/` (standalone production placeholder). The build writes the deployable site to `dist/`, which is gitignored.

## Pages

- `/` home, `/realm`, `/lineage`, `/calendar`, `/shop`, and ten generated product pages under `/products/`
- `/about`, `/social`, `/support`, `/terms`, `/privacy`, `/cookies`, `/order`, and `/404`

Product data comes from [`../docs/product/apparel-manifest.json`](../docs/product/apparel-manifest.json). Shared look and feel (gutter, type scale, the `plain-page` template) lives in `src/layouts/BaseLayout.astro`.

## Develop

Node.js 24 or newer.

```sh
npm install --prefix website
npm run dev --prefix website      # local dev server
npm run build --prefix website    # type-check and build into website/dist/
firebase emulators:start --only hosting
```

Run `python3 scripts/check-site.py` after a build to validate the output.
