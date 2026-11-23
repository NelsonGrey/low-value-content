#!/usr/bin/env python3
"""Replace art on the six existing Printify drafts; never publish or order.

Run without arguments to inspect preconditions. Use --apply after approval.
The token is read from functions/.secret.local and never printed.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SHOP = 29342324
IMAGE_X, IMAGE_Y, IMAGE_SCALE, IMAGE_ANGLE = 0.5, 0.42, 0.82, 0
RECORD = ROOT / "tools/printify/launch-six-products.json"
ART = ROOT / "production/print-files/launch-six-redesign-candidate-v1"
LOG = ROOT / "production/qa/printify-redesign-update-2026-11-23.json"
PRODUCTS = [
    ("validate", "01-approval-pending"),
    ("thought-leader", "02-honorary-appointment"),
    ("doomscrolling", "03-inquiry-feed"),
    ("content-creator", "04-creator-audit"),
    ("authentic-self", "05-authentic-self-tag"),
    ("sent-regretted", "06-one-minute-record"),
]
TITLE_04 = "Content creator. Originality questionable. Revenue inconsistent. Reach unreported."


def token():
    for line in (ROOT / "functions/.secret.local").read_text().splitlines():
        if line.startswith("PRINTIFY_API_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("PRINTIFY_API_TOKEN missing")


def request(session, method, path, payload=None):
    response = session.request(method, f"https://api.printify.com/v1{path}", json=payload, timeout=90)
    if not response.ok:
        raise RuntimeError(f"Printify {method} {path}: HTTP {response.status_code}, {response.text[:350]}")
    return response.json()


def front_image(product):
    return [image for area in product["print_areas"] for placeholder in area["placeholders"]
            if placeholder["position"] == "front" for image in placeholder["images"]]


def check_product(key, product, entry, allowed_ids):
    if product["id"] != entry["productId"] or product["blueprint_id"] != 706 or product["print_provider_id"] != 99:
        raise RuntimeError(f"{key}: unexpected product identity or blank")
    if product.get("is_locked") or product.get("is_deleted"):
        raise RuntimeError(f"{key}: product locked or deleted")
    enabled = {v["id"]: v for v in product["variants"] if v.get("is_enabled")}
    if set(enabled) != set(entry["variants"].values()) or {v["price"] for v in enabled.values()} != {3600}:
        raise RuntimeError(f"{key}: variants or price differ from expected six at $36")
    images = front_image(product)
    if len(images) != 1 or images[0]["id"] not in allowed_ids:
        raise RuntimeError(f"{key}: unexpected front image")
    image = images[0]
    if (image["x"], image["y"], image["scale"], image["angle"]) not in {
        (0.5, 0.5, 0.9452, 0),
        (IMAGE_X, IMAGE_Y, IMAGE_SCALE, IMAGE_ANGLE),
    }:
        raise RuntimeError(f"{key}: placement changed")
    other = [p for area in product["print_areas"] for p in area["placeholders"]
             if p["position"] != "front" and p.get("images")]
    if other:
        raise RuntimeError(f"{key}: another print location has art")


def write_log(data):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps(data, indent=2) + "\n")


def main():
    apply = "--apply" in sys.argv
    record = json.loads(RECORD.read_text())
    progress = json.loads(LOG.read_text()) if LOG.exists() else {}
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token()}", "User-Agent": "lvc-launch-art-update"})
    for key, stem in PRODUCTS:
        entry = record[key]
        png = ART / (stem + ".png")
        with Image.open(png) as image:
            if image.size != (4500, 5400) or image.mode != "RGBA" or "icc_profile" not in image.info:
                raise RuntimeError(f"{key}: local PNG failed basic print check")
        digest = hashlib.sha256(png.read_bytes()).hexdigest()
        prior = progress.get(key, {})
        old_id = prior.get("oldUploadId", entry["uploadId"])
        allowed = {old_id, entry["uploadId"]}
        if prior.get("newUploadId"):
            allowed.add(prior["newUploadId"])
        product = request(session, "GET", f"/shops/{SHOP}/products/{entry['productId']}.json")
        check_product(key, product, entry, allowed)
        current_id = front_image(product)[0]["id"]
        position = (front_image(product)[0]["x"], front_image(product)[0]["y"],
                    front_image(product)[0]["scale"], front_image(product)[0]["angle"])
        if prior.get("newUploadId") == current_id and prior.get("sourceSha256") == digest and position == (IMAGE_X, IMAGE_Y, IMAGE_SCALE, IMAGE_ANGLE):
            print(f"{key}: already updated and verified")
            continue
        print(f"{key}: ready, current art {current_id}, new file {png.name}")
        if not apply:
            continue
        if current_id not in {old_id, prior.get("newUploadId")}:
            raise RuntimeError(f"{key}: current art no longer matches saved original")
        if not prior.get("newUploadId"):
            upload = request(session, "POST", "/uploads/images.json", {
                "file_name": png.name,
                "contents": base64.b64encode(png.read_bytes()).decode("ascii"),
            })
            if (upload.get("width"), upload.get("height")) != (4500, 5400) or not upload.get("id"):
                raise RuntimeError(f"{key}: upload dimensions or id wrong: {upload}")
            prior = {"productId": entry["productId"], "oldUploadId": old_id,
                     "newUploadId": upload["id"], "sourceSha256": digest, "uploaded": True}
            progress[key] = prior
            write_log(progress)
        body = {
            "print_areas": [{
                "variant_ids": product["print_areas"][0]["variant_ids"],
                "placeholders": [{"position": "front", "images": [{
                    "id": prior["newUploadId"], "x": IMAGE_X, "y": IMAGE_Y, "scale": IMAGE_SCALE, "angle": IMAGE_ANGLE,
                }]}],
            }],
        }
        if key == "content-creator":
            body["title"] = TITLE_04
        request(session, "PUT", f"/shops/{SHOP}/products/{entry['productId']}.json", body)
        updated = request(session, "GET", f"/shops/{SHOP}/products/{entry['productId']}.json")
        check_product(key, updated, entry, {prior["newUploadId"]})
        if key == "content-creator" and updated["title"] != TITLE_04:
            raise RuntimeError("04 title did not update")
        prior["verified"] = True
        progress[key] = prior
        write_log(progress)
        entry["uploadId"] = prior["newUploadId"]
        RECORD.write_text(json.dumps(record, indent=2) + "\n")
        print(f"{key}: updated and verified, new art {prior['newUploadId']}")
    if apply:
        print("All six draft updates completed; no publish or order action was called.")


if __name__ == "__main__":
    main()
