#!/usr/bin/env python3
"""Build every favicon file from the one master, website/public/assets/favicon.svg.

Needs rsvg-convert (brew install librsvg) and Pillow. Writes, for both the storefront (website/public) and the
standalone coming-soon page (website/coming-soon):
  favicon.ico            16, 32 and 48 px (PNG-compressed entries)
  apple-touch-icon.png   180 px, full bleed (iOS rounds the corners itself)
  assets/icon-192.png, assets/icon-512.png   full bleed, mark inside the central 80% (safe for masked icons)
  site.webmanifest
The coming-soon page is deployed on its own, so it carries its own copy of each file.
"""
import io, json, pathlib, struct, subprocess, shutil, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
MASTER = ROOT / "website/public/assets/favicon.svg"
TARGETS = [ROOT / "website/public", ROOT / "website/coming-soon"]
NAVY = "#0d1c2b"

def render(svg_text, size):
    p = subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), "-f", "png"], input=svg_text.encode(), capture_output=True, check=True)
    return Image.open(io.BytesIO(p.stdout)).convert("RGBA")

def png_bytes(im):
    b = io.BytesIO(); im.save(b, "PNG", optimize=True); return b.getvalue()

def ico(entries):
    """Build an .ico by hand so each size is rendered natively instead of downscaled from one image."""
    head = struct.pack("<HHH", 0, 1, len(entries))
    offset = 6 + 16 * len(entries)
    dirs, blobs = b"", b""
    for im in entries:
        data = png_bytes(im)
        w, h = im.size
        dirs += struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(data), offset)
        blobs += data; offset += len(data)
    return head + dirs + blobs

master = MASTER.read_text()
assert 'rx="14"' in master, "master must have the rounded background rect"
full_bleed = master.replace(' rx="14"', "")          # square, for touch icons and the manifest

ico_bytes = ico([render(master, s) for s in (16, 32, 48)])
touch = png_bytes(render(full_bleed, 180))
icon192, icon512 = png_bytes(render(full_bleed, 192)), png_bytes(render(full_bleed, 512))
manifest = json.dumps({
    "name": "The Royal House of Engagement",
    "short_name": "Royal House",
    "description": "Official regalia for the chronically online, by Low Value Content.",
    "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}],
    "theme_color": NAVY, "background_color": NAVY, "display": "browser",
}, indent=2) + "\n"

for target in TARGETS:
    (target / "assets").mkdir(parents=True, exist_ok=True)
    if target != MASTER.parent.parent:                       # the storefront already holds the master
        shutil.copy(MASTER, target / "assets/favicon.svg")
    (target / "favicon.ico").write_bytes(ico_bytes)
    (target / "apple-touch-icon.png").write_bytes(touch)
    (target / "assets/icon-192.png").write_bytes(icon192)
    (target / "assets/icon-512.png").write_bytes(icon512)
    (target / "site.webmanifest").write_text(manifest)
    print("wrote favicon set to", target.relative_to(ROOT))
