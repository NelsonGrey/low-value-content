# Website

The first-generation static editorial showcase in `website/dist/` is retained as an archive. Firebase Hosting now publishes the Astro storefront built from `website/royal/` into `website/royal/dist/`.

## Pages

- `dist/index.html`: brand introduction and overview
- `dist/shirts.html`: the six featured launch concepts
- `dist/collections.html`: the ten editorial collection themes
- `dist/guide.html`: public field guide covering the brand, voice, product standards, release model, QR concept, fit, status, and FAQ
- `dist/about.html`: brand purpose, principles, and current development status
- `dist/social.html`: recommended Instagram, TikTok, and LinkedIn channel roles
- `dist/terms.html`, `privacy.html`, `cookies.html`, and `support.html`: pre-launch policy and support placeholders that must be reviewed before commerce
- `dist/404.html`: branded not-found page

Shared site assets are in `dist/assets/`. Source design files remain in [`../design/`](../design/), and the internal brand and content guide is in [`../docs/brand/LOW_VALUE_CONTENT_GUIDE.md`](../docs/brand/LOW_VALUE_CONTENT_GUIDE.md).

Shared assets live outside this folder: shirt art in [`../design/`](../design/), product copy in [`../docs/product/concept-catalog.md`](../docs/product/concept-catalog.md).

Build and preview the deployed site locally:

```sh
npm run build --prefix website/royal
firebase emulators:start --only hosting
```

For a simple preview after building, run `python3 -m http.server 4173 -d website/royal/dist` from the repository root.
