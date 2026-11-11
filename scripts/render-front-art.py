#!/usr/bin/env python3
"""Build the storefront display PNGs for the holiday six and rebuild the ten-issue proof sheet.

    python3 scripts/render-front-art.py

The print masters live in production/print-files/launch-six-v1/ (outlined SVG plus a
4500x5400 transparent PNG). This script only makes the website copies: a 1200x1440
transparent PNG per design in website/public/assets/, which the site paints the garment
colour behind, and the ten-up proof sheet (the six launch designs plus the held-back
Nos. 07-10). Needs Pillow only.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PRINT = ROOT / "production" / "print-files" / "launch-six-v1"
ASSETS = ROOT / "website" / "public" / "assets"

# (print master stem, display file, garment colour). Garment palette: Ivory, Oxblood, Navy, Black.
LAUNCH = [
    ("01-progress-bar", "front-art-01-validate-me.png", "#f4eedf"),
    ("02-door-plaque", "front-art-02-thought-leader.png", "#10263a"),
    ("03-field-dispatch", "front-art-03-market-research.png", "#7d2734"),
    ("04-editors-marks", "front-art-04-content-creator.png", "#f4eedf"),
    ("05-price-tag", "front-art-05-authentic-self.png", "#7d2734"),
    ("06-giant-times", "front-art-06-sent-regretted.png", "#10263a"),
]
HELD_BACK = [
    ("front-art-07-much-published.png", "#10263a"),
    ("front-art-08-order-blue-check.png", "#151515"),
    ("front-art-09-y2k-postponed.png", "#7d2734"),
    ("front-art-10-saint-moth.png", "#f4eedf"),
]


def display_pngs():
    for stem, display, _ in LAUNCH:
        art = Image.open(PRINT / f"{stem}.png").convert("RGBA").resize((1200, 1440), Image.Resampling.LANCZOS)
        art.save(ASSETS / display, optimize=True)


def sheet():
    tiles = [(display, garment) for _, display, garment in LAUNCH] + HELD_BACK
    gx, gy, w, h = 40, 32, 750, 900
    out = Image.new("RGB", (5 * w + 6 * gx, 2 * h + 3 * gy), (232, 222, 202))
    for i, (file, garment) in enumerate(tiles):
        tile = Image.new("RGBA", (w, h), garment)
        art = Image.open(ASSETS / file).convert("RGBA").resize((w, h), Image.Resampling.LANCZOS)
        tile.alpha_composite(art)
        out.paste(tile.convert("RGB"), (gx + (i % 5) * (w + gx), gy + (i // 5) * (h + gy)))
    out.save(ASSETS / "front-art-founding-ten.png", optimize=True)


if __name__ == "__main__":
    display_pngs()
    sheet()
    print("wrote 6 display PNGs and the ten-issue proof sheet")
