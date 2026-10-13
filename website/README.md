# Website

Static site served by Firebase Hosting from `website/dist/`. It is currently a placeholder landing page; the final stack has not been chosen. If a framework is adopted, scaffold it here and point `hosting.public` in [`../firebase.json`](../firebase.json) at its build output.

Shared assets live outside this folder: shirt art in [`../design/`](../design/), product copy in [`../docs/product/concept-catalog.md`](../docs/product/concept-catalog.md).

Preview locally: `firebase emulators:start --only hosting`
