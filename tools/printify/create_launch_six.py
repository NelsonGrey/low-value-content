#!/usr/bin/env python3
"""Create the holiday-six products in the Printify shop (unpublished drafts).

    python3 tools/printify/create_launch_six.py            # dry run: prints what it would do
    python3 tools/printify/create_launch_six.py --apply    # uploads art, creates missing products

Blank: Comfort Colors 1717 (blueprint 706), provider Printify Choice (99). Each product enables
only the garment colour that design is meant for, in sizes S-3XL: Ivory, True Navy and Brick
(the closest Comfort Colors shade to oxblood; Printify's own mockups showed "Navy" as a grey-blue
and "Crimson" as a coral red). Brick is provisional until a physical sample is seen.

The token comes from functions/.secret.local (PRINTIFY_API_TOKEN) and is never printed.
Created product ids are recorded in tools/printify/launch-six-products.json, and products
already recorded there are skipped, so re-running is safe. Nothing is published to a sales
channel and no order is placed.
"""
import base64, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SHOP_ID = 29342324
BLUEPRINT, PROVIDER = 706, 99
SIZES = ["S", "M", "L", "XL", "2XL", "3XL"]
PRICE_CENTS = 3200
# Front print area on provider 99 is 3703x4200 px; our 4500x5400 art is fitted to its height.
IMAGE_SCALE = round((4200 * 4500 / 5400) / 3703, 4)
RECORD = Path(__file__).with_name("launch-six-products.json")

PRODUCTS = [
    # key, no., title, print file, candidate colours
    ("validate", "01", "Please validate me algorithmically.", "01-progress-bar", ["Ivory"]),
    ("thought-leader", "02", "Thought leader. No thoughts required.", "02-door-plaque", ["True Navy"]),
    ("doomscrolling", "03", "I'm not doomscrolling. I'm doing market research.", "03-field-dispatch", ["Brick"]),
    ("content-creator", "04", "Content creator. Uniqueness questionable. Monetization inconsistent. Visibility unreported.", "04-editors-marks", ["Ivory"]),
    ("authentic-self", "05", "My authentic self is currently being monetized.", "05-price-tag", ["Brick"]),
    ("sent-regretted", "06", "Sent 2:14 AM. Regretted 2:15 AM.", "06-giant-times", ["True Navy"]),
]


def token():
    for line in (ROOT / "functions" / ".secret.local").read_text().splitlines():
        if line.startswith("PRINTIFY_API_TOKEN="):
            return line.split("=", 1)[1].strip()
    sys.exit("PRINTIFY_API_TOKEN not found in functions/.secret.local")


def call(method, path, body=None):
    cmd = ["curl", "-s", "-X", method, "-H", f"Authorization: Bearer {TOKEN}", "-H", "User-Agent: lvc-launch",
           "-H", "Content-Type: application/json", f"https://api.printify.com/v1{path}"]
    if body is not None:
        cmd += ["--data-binary", "@-"]
    out = subprocess.run(cmd, input=json.dumps(body) if body is not None else None, capture_output=True, text=True).stdout
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        sys.exit(f"Unexpected response from {method} {path}: {out[:200]}")


def main():
    global TOKEN
    apply = "--apply" in sys.argv
    TOKEN = token()
    record = json.loads(RECORD.read_text()) if RECORD.exists() else {}
    catalog = call("GET", f"/catalog/blueprints/{BLUEPRINT}/print_providers/{PROVIDER}/variants.json")["variants"]
    by_option = {(v["options"]["color"], v["options"]["size"]): v["id"] for v in catalog}
    for key, number, title, stem, colours in PRODUCTS:
        if key in record:
            print(f"{number} {key}: already created ({record[key]['productId']})")
            continue
        ids = {f"{c}|{s}": by_option[(c, s)] for c in colours for s in SIZES}
        print(f"{number} {key}: {len(ids)} variants ({', '.join(colours)}), art {stem}.png, scale {IMAGE_SCALE}")
        if not apply:
            continue
        png = ROOT / "production" / "print-files" / "launch-six-v1" / f"{stem}.png"
        up = call("POST", "/uploads/images.json", {"file_name": f"{stem}.png", "contents": base64.b64encode(png.read_bytes()).decode()})
        body = {
            "title": title,
            "description": f"The Royal House of Engagement, No. {number}. Comfort Colors 1717 garment-dyed tee, front print. Low Value Content.",
            "blueprint_id": BLUEPRINT, "print_provider_id": PROVIDER,
            "variants": [{"id": v, "price": PRICE_CENTS, "is_enabled": True} for v in ids.values()],
            "print_areas": [{"variant_ids": list(ids.values()),
                             "placeholders": [{"position": "front", "images": [{"id": up["id"], "x": 0.5, "y": 0.5, "scale": IMAGE_SCALE, "angle": 0}]}]}],
        }
        made = call("POST", f"/shops/{SHOP_ID}/products.json", body)
        if "id" not in made:
            sys.exit(f"{key}: create failed: {json.dumps(made)[:300]}")
        record[key] = {"productId": made["id"], "uploadId": up["id"], "variants": {k: v for k, v in ids.items()}}
        RECORD.write_text(json.dumps(record, indent=2) + "\n")
        print(f"   created {made['id']}")


if __name__ == "__main__":
    main()
