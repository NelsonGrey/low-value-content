#!/usr/bin/env python3
"""Build the November holiday-six front-art candidates without changing prototypes."""
from pathlib import Path
import subprocess
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "production/print-files/holiday-six-v1"
PROTO = ROOT / "design/prototypes"
PLATE = ROOT / "design/mockups/royal-house/A07-much-published-little-said.png"
EDITED_PLATE = OUT / '07-edited-source-plate.png'
GENERATED_PLATE = Path(__import__('sys').argv[1]) if len(__import__('sys').argv) > 1 else (EDITED_PLATE if EDITED_PLATE.exists() else PLATE)
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()


def svg(number, old, new, replacements, remove_mark=False):
    s = (PROTO / old).read_text()
    for before, after in replacements:
        assert before in s, (number, before)
        s = s.replace(before, after)
    if remove_mark:
        start = s.index('  <g id="house-mark"')
        end = s.index('  <g id="house-frame"', start)
        s = s[:start] + s[end:]
    target = OUT / f"{number}-{new}.svg"
    target.write_text(s)
    subprocess.run(['rsvg-convert', '-w', '4500', '-h', '5400', '-o', str(target.with_suffix('.png')), str(target)], check=True)
    with Image.open(target.with_suffix('.png')) as rendered:
        rendered.save(target.with_suffix('.png'), dpi=(300, 300), icc_profile=SRGB, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    svg('01', '01-validate-me.svg', 'validate-me', [], True)
    svg('02', '02-thought-leader.svg', 'thought-leader', [
        ('<text x="2250" y="4310" fill="#142B40"', '<text x="2250" y="4310" fill="#BD9143"'),
    ], False)
    svg('03', '03-market-research.svg', 'market-research', [
        ('I’m not doomscrolling.', "I'm not doomscrolling."),
        ('I’M DOING', "I'M DOING"),
    ])
    svg('05', '05-authentic-self.svg', 'authentic-self', [
        ('<g text-anchor="middle" font-family="Arial, Helvetica, sans-serif">',
         '<defs><mask id="monetized-knockout" maskUnits="userSpaceOnUse" x="760" y="2100" width="2980" height="900"><rect x="760" y="2100" width="2980" height="900" fill="white"/><text x="2250" y="2710" font-family="Arial, Helvetica, sans-serif" font-size="380" font-weight="800" letter-spacing="4" text-anchor="middle" fill="black">MONETIZED</text></mask></defs>\n  <g text-anchor="middle" font-family="Arial, Helvetica, sans-serif">'),
        ('<rect x="760" y="2100" width="2980" height="900" fill="#852E34"/>',
         '<rect x="760" y="2100" width="2980" height="900" fill="#852E34" mask="url(#monetized-knockout)"/>'),
        ('    <text x="2250" y="2710" fill="#F4EEDF" font-size="420" font-weight="800" letter-spacing="4" data-production="garment-color knockout; not a third ink">MONETIZED</text>\n', ''),
    ], True)
    svg('19', '19-seen-regretted.svg', 'sent-regretted', [
        ('Seen 2:14 AM.', 'Sent 2:14 AM.'),
        ('SEEN 2:14 AM.', 'SENT 2:14 AM.'),
        ('DELIVERED · READ · REGRETTED', 'SENT · DELIVERED · READ · REGRETTED'),
        ('font-size="96" letter-spacing="22"', 'font-size="83" letter-spacing="14"'),
        ('#F4EEDF', '#E7D9BA'),
    ], True)

    # Keep the selected plate's proportions. The edited plate is source-sized;
    # enlarging it does not create native high-resolution illustration detail.
    if GENERATED_PLATE != EDITED_PLATE:
        EDITED_PLATE.write_bytes(GENERATED_PLATE.read_bytes())
    im = Image.open(EDITED_PLATE).convert('RGBA')
    scale = min(4500 / im.width, 5400 / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (4500, 5400))
    canvas.alpha_composite(im, ((4500 - im.width)//2, (5400 - im.height)//2))
    canvas.save(OUT / '07-much-published.png', dpi=(300, 300), icc_profile=SRGB, optimize=True)
    print(OUT)


if __name__ == '__main__':
    main()
