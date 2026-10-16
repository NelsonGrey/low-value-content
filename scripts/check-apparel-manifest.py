#!/usr/bin/env python3
"""Validate the apparel manifest against creative assets and commerce wiring."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "docs" / "product" / "apparel-manifest.json"
CATALOG_PATH = ROOT / "docs" / "product" / "concept-catalog.md"
COMMERCE_PATH = ROOT / "functions" / "src" / "catalog.ts"
STOREFRONT_PATH = ROOT / "website" / "dist" / "shirts.html"


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    products = manifest.get("launchProducts", [])

    if len(products) != 10:
        errors.append(f"launchProducts must contain 10 products, found {len(products)}")

    ids = [product.get("id") for product in products]
    if len(ids) != len(set(ids)):
        errors.append("launch product IDs must be unique")

    positions = [product.get("position") for product in products]
    if positions != list(range(1, 11)):
        errors.append(f"launch positions must be 1 through 10 in order, found {positions}")

    families = {family["id"] for family in manifest.get("productFamilies", [])}
    reigns = {entry["id"] for entry in manifest.get("lineage", [])}
    houses = {entry["name"] for entry in manifest.get("houses", [])}
    sovereign_house = manifest.get("brand", {}).get("brandWorld")
    qr_routes: set[str] = set()

    for product in products:
        label = product.get("id", "<missing-id>")
        for field in ("primaryCopy", "originalCollection", "family", "royalTreatment", "house", "qrRoute", "creativeStatus", "commerceStatus"):
            if not product.get(field):
                errors.append(f"{label}: missing {field}")
        if product.get("family") not in families:
            errors.append(f"{label}: unknown family {product.get('family')!r}")
        if product.get("reign") not in reigns:
            errors.append(f"{label}: unknown reign {product.get('reign')!r}")
        if product.get("house") not in houses | {sovereign_house}:
            errors.append(f"{label}: unknown house {product.get('house')!r}")
        realm_issue = product.get("realmIssue", {})
        for field in ("office", "wearerTitle", "proclamation"):
            if not realm_issue.get(field):
                errors.append(f"{label}: missing realmIssue.{field}")
        route = product.get("qrRoute")
        if route in qr_routes:
            errors.append(f"{label}: duplicate QR route {route!r}")
        qr_routes.add(route)
        for asset_name, asset_path in product.get("assets", {}).items():
            if not (ROOT / asset_path).is_file():
                errors.append(f"{label}: missing {asset_name} asset {asset_path}")

    for group_name, paths in manifest.get("sharedAssets", {}).items():
        if group_name.endswith("Glob"):
            if not list(ROOT.glob(paths)):
                errors.append(f"sharedAssets.{group_name}: glob matched no files: {paths}")
            continue
        for asset_path in paths:
            if not (ROOT / asset_path).is_file():
                errors.append(f"sharedAssets.{group_name}: missing {asset_path}")

    concept_text = CATALOG_PATH.read_text(encoding="utf-8")
    saying_numbers = [int(n) for n in re.findall(r"^\|\s*(\d+)\s*\|", concept_text, flags=re.MULTILINE)]
    if saying_numbers != list(range(1, 101)):
        errors.append("concept catalog must retain exactly the numbered sayings 1 through 100")

    storefront_text = STOREFRONT_PATH.read_text(encoding="utf-8")
    storefront_ids = set(re.findall(r'data-product="([^"]+)"', storefront_text))
    missing_storefront = storefront_ids - set(ids)
    if missing_storefront:
        errors.append(f"storefront product IDs absent from manifest: {sorted(missing_storefront)}")

    commerce_text = COMMERCE_PATH.read_text(encoding="utf-8")
    commerce_keys = set(re.findall(r"^\s{2}([a-zA-Z][\w-]*):\s*\{", commerce_text, flags=re.MULTILINE))
    by_catalog_key = {
        product["commerce"]["catalogKey"]: product
        for product in products
        if product.get("commerce", {}).get("catalogKey")
    }
    missing_manifest = commerce_keys - set(by_catalog_key)
    if missing_manifest:
        errors.append(f"backend commerce keys absent from manifest: {sorted(missing_manifest)}")

    for key in commerce_keys & set(by_catalog_key):
        product = by_catalog_key[key]
        product_id = product["commerce"].get("printifyProductId")
        if product_id and product_id not in commerce_text:
            errors.append(f"{product['id']}: Printify product ID does not match backend catalog")

    for error in errors:
        print(f"ERROR {error}")
    print(
        f"checked {len(products)} launch products, {len(saying_numbers)} sayings, "
        f"{len(storefront_ids)} storefront commerce ID(s), {len(errors)} problem(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
