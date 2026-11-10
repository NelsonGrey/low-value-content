#!/usr/bin/env python3
"""Render the two-ink SVG front art (Nos. 01-06) to the storefront display PNGs and
rebuild the ten-issue proof sheet.

    python3 scripts/render-front-art.py

Needs Playwright (chromium) and Pillow. Display PNGs are 750x900 with a transparent
background; the site paints the garment colour behind them. Print files are a separate
step (outline type, provider template) and are not produced here.
"""
import io
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / "design" / "prototypes"
ASSETS = ROOT / "website" / "public" / "assets"
NAMES = ["01-validate-me", "02-thought-leader", "03-market-research", "04-content-creator", "05-authentic-self", "06-optimized-shirt"]
FRONT = {n: f"front-art-{n}.png" for n in NAMES}
FRONT.update({
    "07": "front-art-07-much-published.png", "08": "front-art-08-order-blue-check.png",
    "09": "front-art-09-y2k-postponed.png", "10": "front-art-10-saint-moth.png",
})
# Garment palette: Ivory, Oxblood, Navy, Black.
GARMENT = ["#f4eedf", "#f4eedf", "#7d2734", "#f4eedf", "#f4eedf", "#f4eedf", "#10263a", "#151515", "#7d2734", "#f4eedf"]


def render():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 750, "height": 900})
        for n in NAMES:
            svg = (PROTO / f"{n}.svg").read_text().replace('width="4500" height="5400"', 'width="750" height="900"')
            pg.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
            (ASSETS / FRONT[n]).write_bytes(pg.screenshot(omit_background=True, clip={"x": 0, "y": 0, "width": 750, "height": 900}))
        b.close()


def sheet():
    files = [FRONT[n] for n in NAMES] + [FRONT[k] for k in ("07", "08", "09", "10")]
    gx, gy, w, h = 40, 32, 750, 900
    out = Image.new("RGB", (5 * w + 6 * gx, 2 * h + 3 * gy), (232, 222, 202))
    for i, f in enumerate(files):
        tile = Image.new("RGBA", (w, h), GARMENT[i])
        art = Image.open(ASSETS / f).convert("RGBA").resize((w, h))
        tile.alpha_composite(art)
        out.paste(tile.convert("RGB"), (gx + (i % 5) * (w + gx), gy + (i // 5) * (h + gy)))
    out.save(ASSETS / "front-art-founding-ten.png", optimize=True)


if __name__ == "__main__":
    render()
    sheet()
    print("rendered 6 display PNGs and the proof sheet")
