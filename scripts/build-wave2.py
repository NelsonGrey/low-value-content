#!/usr/bin/env python3
"""Generate the Wave 2 proof artwork (Nos. 11-20) as two-ink SVGs on the shared House frame.

    python3 scripts/build-wave2.py            # writes design/prototypes/11-*.svg ... 20-*.svg
    python3 scripts/build-wave2.py --preview  # also writes previews and a proof sheet (needs Playwright, Pillow)

Proofs for approval, not final art: type is live text and must be outlined before printing.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "design" / "prototypes"
NAVY, OX, GOLD, IVORY = "#142B40", "#852E34", "#C99B43", "#F4EEDF"
GARMENT = {"ivory": "#f4eedf", "navy": "#10263a", "oxblood": "#7d2734", "black": "#151515"}
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "Arial, Helvetica, sans-serif"
MONO = "'Courier New', Courier, monospace"


def frame(ink, n, mark_ink=None, mark_y=None, imprint=None):
    X0, Y0, X1, Y1 = 250, 400, 4250, 5050
    dia = "".join(f'<path d="M{x} {y-95}l95 95-95 95-95-95z"/>' for x, y in [(X0, Y0), (X1, Y0), (X0, Y1), (X1, Y1)])
    mark = ""
    if mark_y is not None:
        m = mark_ink or ink
        mark = (f'<g id="house-mark" transform="translate(2040 {mark_y}) scale(4.2)" fill="none" stroke="{m}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
                '<path d="M26 31a34 34 0 0 1 48 0M34 39a23 23 0 0 1 32 0M43 47a10 10 0 0 1 14 0"/><path d="M22 55h56v31H22zM38 86 50 96l12-10"/>'
                f'<circle cx="74" cy="56" r="9" fill="{m}" stroke="none"/></g>')
    return f'''  {mark}
  <g id="house-frame">
    <g fill="none" stroke="{ink}"><rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" stroke-width="34"/><rect x="{X0+85}" y="{Y0+85}" width="{X1-X0-170}" height="{Y1-Y0-170}" stroke-width="11"/></g>
    <g fill="{ink}">{dia}<path d="M700 4800l60 60-60 60-60-60z"/><path d="M3800 4800l60 60-60 60-60-60z"/></g>
    <text x="2250" y="4850" fill="{imprint or ink}" font-family="{SERIF}" font-size="80" letter-spacing="26" text-anchor="middle">THE ROYAL HOUSE OF ENGAGEMENT · NO. {n:02d}</text>
  </g>
'''


def t(x, y, s, size, fill, family=SANS, weight="", anchor="middle", ls=0, style="", extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    st = f' font-style="{style}"' if style else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" font-size="{size}"{w}{st}{l} text-anchor="{anchor}"{extra}>{s}</text>'


def svg(title, desc, body, fr):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="4500" height="5400" viewBox="0 0 4500 5400">
  <title>{title}</title>
  <desc>{desc}</desc>
{body}
{fr}</svg>
'''


def d11():
    b = [f'<rect x="1810" y="1280" width="880" height="880" fill="none" stroke="{NAVY}" stroke-width="44"/>',
         f'<path d="M1990 1730l220 230 330-500" fill="none" stroke="{OX}" stroke-width="64" stroke-linecap="round" stroke-linejoin="round"/>',
         t(2250, 2760, "I HAVE READ AND", 330, NAVY, SANS, "800"), t(2250, 3140, "ACCEPTED NOTHING.", 330, NAVY, SANS, "800")]
    fine = ["1.1 The party of the first part agrees to nothing in particular.", "1.2 The party of the second part has stopped reading.",
            "2.1 Continued scrolling constitutes acceptance of continued scrolling.", "2.2 Terms are subject to change without the courtesy of notice.",
            "3.1 This agreement supersedes every agreement you have agreed to.", "3.2 Please scroll down to the bottom. There is no bottom."]
    for i, line in enumerate(fine):
        b.append(f'<text x="700" y="{3560 + i*118}" fill="{NAVY}" font-family="{SERIF}" font-size="76" textLength="3100" lengthAdjust="spacingAndGlyphs">{line}</text>')
    b.append(t(2250, 4440, "☐  I AGREE TO THE TERMS OF THE TERMS", 88, OX, SANS, "700", ls=14).replace("☐", "■"))
    return svg("I have read and accepted nothing", "Agreement checkbox above legal microtype.", "\n  ".join(b), frame(OX, 11, OX, 780))


def d12():
    b = [t(2250, 1560, "MY PRIVACY", 440, IVORY, SERIF, "700"), t(2250, 2060, "HAS ADS.", 440, GOLD, SERIF, "700")]
    b.append(f'<rect x="760" y="2450" width="2980" height="1700" fill="none" stroke="{IVORY}" stroke-width="26"/>')
    b.append(t(900, 2640, "PRIVACY SETTINGS", 90, IVORY, SANS, "700", "start", 20))
    rows = ["Share my data", "Share my data again", "Share my data (recommended)"]
    for i, r in enumerate(rows):
        y = 2840 + i * 330
        b.append(t(900, y + 70, r, 110, IVORY, SERIF, anchor="start"))
        b.append(f'<rect x="3150" y="{y}" width="400" height="110" rx="55" fill="{GOLD}"/><circle cx="3495" cy="{y+55}" r="42" fill="{NAVY}"/>')
    b.append(f'<g transform="rotate(-5 2250 3250)"><rect x="520" y="3050" width="3460" height="330" fill="{GOLD}"/>{t(2250, 3270, "SPONSORED · YOUR PRIVACY IS OUR PRIORITY*", 112, NAVY, SANS, "800", ls=14)}</g>')
    b.append(t(2250, 4440, "*SPONSORED BY OUR PARTNERS · 4,127 OF THEM", 84, GOLD, SANS, "", ls=18))
    return svg("My privacy has ads", "Privacy-settings panel with a sponsored banner.", "\n  ".join(b), frame(GOLD, 12, GOLD, 780))


def d13():
    b = [t(2250, 1700, "CANCEL ANYTIME", 330, NAVY, SANS, "800"), t(2250, 2080, "AFTER CALLING US.", 330, NAVY, SANS, "800")]
    b.append(f'<rect x="1560" y="2400" width="1380" height="380" fill="{OX}"/>{t(2250, 2650, "CANCEL", 190, IVORY, SANS, "800", ls=36)}')
    b.append(f'<path d="M2250 2800v220" stroke="{NAVY}" stroke-width="28"/>')
    for i, (x, y) in enumerate([(1250, 3500), (2250, 3500), (3250, 3500)]):
        b.append(f'<path d="M2250 3020 L{x} {y-150}" stroke="{NAVY}" stroke-width="22" fill="none"/><circle cx="{x}" cy="{y}" r="150" fill="none" stroke="{NAVY}" stroke-width="26"/>{t(x, y+58, str(i+1), 170, NAVY, SANS, "800")}')
        for dx in (-260, 0, 260):
            b.append(f'<path d="M{x} {y+150} L{x+dx} {y+420}" stroke="{OX}" stroke-width="16" fill="none"/><circle cx="{x+dx}" cy="{y+470}" r="46" fill="{OX}"/>')
    b.append(t(2250, 4390, "PRESS 7 TO HEAR THESE OPTIONS AGAIN", 92, OX, SANS, "700", ls=18))
    return svg("Cancel anytime after calling us", "Cancel button leading into a telephone tree.", "\n  ".join(b), frame(OX, 13, OX, 780))


def d14():
    cx, cy, r = 2250, 1780, 560
    b = [f'<path d="M{cx-190} {cy-80} l190 -110 190 110 v220 l-190 110 -190 -110z M{cx-190} {cy-80} l190 110 190 -110 M{cx} {cy+30} v220" fill="none" stroke="{IVORY}" stroke-width="40" stroke-linejoin="round"/>']
    import math
    for k in range(3):
        a0 = math.radians(-90 + k * 120 + 18); a1 = math.radians(-90 + (k + 1) * 120 - 18)
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        b.append(f'<path d="M{x0:.0f} {y0:.0f} A{r} {r} 0 0 1 {x1:.0f} {y1:.0f}" fill="none" stroke="{GOLD}" stroke-width="44" stroke-linecap="round"/>')
        ang = a1 + math.radians(90)
        hx, hy = x1, y1; s = 120
        p1 = (hx + s * math.cos(ang - 2.6), hy + s * math.sin(ang - 2.6)); p2 = (hx + s * math.cos(ang + 2.6), hy + s * math.sin(ang + 2.6)); p0 = (hx + s * 0.9 * math.cos(ang), hy + s * 0.9 * math.sin(ang))
        b.append(f'<path d="M{p1[0]:.0f} {p1[1]:.0f} L{p0[0]:.0f} {p0[1]:.0f} L{p2[0]:.0f} {p2[1]:.0f}" fill="none" stroke="{GOLD}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>')
    b += [t(2250, 3010, "REDUCE.", 400, IVORY, SERIF, "700"), t(2250, 3490, "REUSE.", 400, IVORY, SERIF, "700"), t(2250, 3970, "OVERNIGHT", 400, GOLD, SERIF, "700"), t(2250, 4440, "DELIVERY.", 400, GOLD, SERIF, "700")]
    return svg("Reduce. Reuse. Overnight delivery.", "Recycling arrows around a shipping box.", "\n  ".join(b), frame(GOLD, 14))


def d15():
    cx, cy = 2250, 1560
    circ = 2 * 3.14159 * 360
    b = [f'<circle cx="{cx}" cy="{cy}" r="500" fill="none" stroke="{GOLD}" stroke-width="22"/>',
         f'<circle cx="{cx}" cy="{cy}" r="360" fill="none" stroke="{IVORY}" stroke-width="90" stroke-dasharray="{circ*0.72:.0f} {circ*0.28:.0f}" transform="rotate(-90 {cx} {cy})"/>',
         t(cx, cy + 66, "72%", 190, GOLD, SERIF, "700"),
         t(2250, 2420, "COMMISSION FOR IMMINENT AVAILABILITY", 84, GOLD, SANS, "", ls=16),
         t(2250, 3060, "MY SELF-WORTH", 420, IVORY, SERIF, "700"), t(2250, 3560, "IS BUFFERING.", 420, IVORY, SERIF, "700"),
         f'<path d="M1100 3880h2300" stroke="{GOLD}" stroke-width="22"/>',
         t(2250, 4210, "BARON OF BUFFERING", 150, GOLD, SERIF, ls=44), t(2250, 4440, "ESTIMATED CONFIRMATION · EVENTUALLY, PERHAPS", 80, GOLD, SANS, ls=16)]
    return svg("My self-worth is buffering", "Appointment of the Baron of Buffering.", "\n  ".join(b), frame(GOLD, 15))


def d16():
    b = []
    for i, h in enumerate([220, 380, 540, 700]):
        x = 1700 + i * 280
        b.append(f'<rect x="{x}" y="{2080-h}" width="170" height="{h}" fill="none" stroke="{IVORY}" stroke-width="26"/>')
    b.append(f'<path d="M1560 2160L3000 1000" stroke="{GOLD}" stroke-width="40" stroke-linecap="round"/>')
    b += [t(2250, 2840, "OFFLINE IS", 430, IVORY, SANS, "800"), t(2250, 3300, "CURRENTLY", 430, IVORY, SANS, "800"), t(2250, 3760, "UNAVAILABLE.", 430, GOLD, SANS, "800"),
          f'<path d="M1000 4000h2500" stroke="{GOLD}" stroke-width="22"/>', t(2250, 4290, "ESTIMATED RETURN · EVENTUALLY, PERHAPS", 100, GOLD, SERIF, ls=18)]
    return svg("Offline is currently unavailable", "Empty signal bars struck through, with system-status wording.", "\n  ".join(b), frame(GOLD, 16))


def d17():
    b = [t(620, 1380, "SERVICE NOTICE 0017", 120, OX, MONO, "700", "start", 28),
         t(620, 2060, "ORIGINAL THOUGHT", 300, NAVY, MONO, "700", "start"), t(620, 2450, "TEMPORARILY", 300, NAVY, MONO, "700", "start"), t(620, 2840, "UNAVAILABLE.", 300, NAVY, MONO, "700", "start"),
         '<defs><pattern id="hz" width="120" height="120" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="60" height="120" fill="%s"/></pattern></defs>' % OX,
         f'<rect x="620" y="3200" width="3260" height="300" fill="url(#hz)"/>',
         t(620, 3860, "ESTIMATED RETURN: UNKNOWN", 150, NAVY, MONO, "700", "start", 12), t(620, 4130, "WE APOLOGISE FOR THE INCONVENIENCE OF YOUR OWN MIND_", 96, OX, MONO, "", "start", 6)]
    return svg("Original thought temporarily unavailable", "Maintenance notice with hazard stripe.", "\n  ".join(b), frame(OX, 17, OX, 780))


def d18():
    b = [t(2250, 1760, "I CAME.", 400, IVORY, SERIF, "700", ls=40), t(2250, 2290, "I SAW.", 400, IVORY, SERIF, "700", ls=40), t(2250, 2820, "I REFRESHED.", 400, GOLD, SERIF, "700", ls=10),
         f'<path d="M900 3050h2700" stroke="{GOLD}" stroke-width="22"/>']
    cx, cy, r = 2250, 3600, 300
    b.append(f'<path d="M{cx+r} {cy-30} A{r} {r} 0 1 1 {cx+r*0.42:.0f} {cy-r*0.9:.0f}" fill="none" stroke="{GOLD}" stroke-width="48" stroke-linecap="round"/><path d="M{cx+r*0.05:.0f} {cy-r*1.5:.0f} L{cx+r*0.62:.0f} {cy-r*0.95:.0f} L{cx-r*0.15:.0f} {cy-r*0.72:.0f}" fill="none" stroke="{GOLD}" stroke-width="48" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(t(2250, 4390, "SEMPER DEORSUM", 110, GOLD, SANS, ls=40))
    return svg("I came. I saw. I refreshed.", "Classical inscription with a refresh glyph.", "\n  ".join(b), frame(GOLD, 18, GOLD, 760))


def d19():
    b = [t(700, 2040, "SEEN 2:14 AM.", 340, IVORY, SANS, "800", "start"), t(700, 2560, "REGRETTED", 340, GOLD, SANS, "800", "start"), t(700, 3080, "2:15 AM.", 340, GOLD, SANS, "800", "start"),
         f'<path d="M700 3380h3100" stroke="{IVORY}" stroke-width="16"/>', t(700, 3640, "DELIVERED · READ · REGRETTED", 96, IVORY, SANS, "", "start", 22),
         f'<path d="M3500 3610l45 45 90-110M3590 3610l45 45 90-110" fill="none" stroke="{GOLD}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round" transform="translate(-20 -24)"/>']
    return svg("Seen 2:14 AM. Regretted 2:15 AM.", "Read-receipt timestamps.", "\n  ".join(b), frame(GOLD, 19, GOLD, 760))


def d20():
    b = [t(620, 1900, "HUMAN FORM.", 330, NAVY, SERIF, "700", "start"), t(620, 2320, "PRINTER", 330, GOLD, SERIF, "700", "start"), t(620, 2740, "RELIABILITY.", 330, GOLD, SERIF, "700", "start")]
    b.append(f'<g fill="none" stroke="{NAVY}" stroke-width="34" stroke-linecap="round" stroke-linejoin="round" transform="translate(2650 2980)"><circle cx="500" cy="140" r="110"/><path d="M500 250v420M320 330h360M500 670l-120 330M500 670l120 330"/></g>')
    b.append(f'<g transform="translate(3000 3690)"><path d="M0 0l180 -300 180 300z" fill="none" stroke="{GOLD}" stroke-width="30" stroke-linejoin="round"/><path d="M180 -200v110" stroke="{GOLD}" stroke-width="30" stroke-linecap="round"/><circle cx="180" cy="-40" r="18" fill="{GOLD}"/></g>')
    rows = [("FORM FACTOR", "HUMAN"), ("JAM INTERVAL", "11 MINUTES"), ("STATUS", "PAPER JAM")]
    for i, (k, v) in enumerate(rows):
        y = 3440 + i * 280
        b.append(t(620, y, k, 100, NAVY, SANS, "700", "start", 16) + t(2420, y, v, 100, NAVY, SANS, "700", "end", 16))
        b.append(f'<path d="M620 {y+50}h1800" stroke="{GOLD}" stroke-width="12"/>')
    return svg("Human form. Printer reliability.", "Specification sheet with a paper-jam warning.", "\n  ".join(b), frame(GOLD, 20, imprint=NAVY))


DESIGNS = [
    (11, "11-read-accepted-nothing", d11, "ivory"), (12, "12-privacy-has-ads", d12, "navy"), (13, "13-cancel-after-calling", d13, "ivory"),
    (14, "14-reduce-reuse-overnight", d14, "black"), (15, "15-self-worth-buffering", d15, "oxblood"), (16, "16-offline-unavailable", d16, "navy"),
    (17, "17-original-thought-unavailable", d17, "ivory"), (18, "18-came-saw-refreshed", d18, "oxblood"), (19, "19-seen-regretted", d19, "navy"),
    (20, "20-human-form-printer", d20, "ivory"),
]

if __name__ == "__main__":
    for n, name, fn, _ in DESIGNS:
        (OUT / f"{name}.svg").write_text(fn())
    print(f"wrote {len(DESIGNS)} SVGs to {OUT}")
    if "--preview" in sys.argv:
        from PIL import Image
        from playwright.sync_api import sync_playwright
        import io
        prev = OUT / "previews"; prev.mkdir(exist_ok=True)
        tiles = []
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 750, "height": 900})
            for n, name, fn, g in DESIGNS:
                s = (OUT / f"{name}.svg").read_text().replace('width="4500" height="5400"', 'width="750" height="900"')
                pg.set_content(f'<html><body style="margin:0;background:transparent">{s}</body></html>')
                png = pg.screenshot(omit_background=True, clip={"x": 0, "y": 0, "width": 750, "height": 900})
                (prev / f"{name}.png").write_bytes(png)
                tile = Image.new("RGBA", (750, 900), GARMENT[g]); tile.alpha_composite(Image.open(io.BytesIO(png)).convert("RGBA")); tiles.append(tile)
            b.close()
        sheet = Image.new("RGB", (5 * 750 + 6 * 40, 2 * 900 + 3 * 32), (232, 222, 202))
        for i, tl in enumerate(tiles):
            sheet.paste(tl.convert("RGB"), (40 + (i % 5) * 790, 32 + (i // 5) * 932))
        sheet.save(prev / "wave-2-proof-sheet.png", optimize=True); print("previews written")
