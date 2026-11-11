"""Helpers: font-to-path, frame, marks, knockouts. Frame/imprint construction
reused from /workspace/lvc-launch-six/build.py (no layouts copied)."""
from __future__ import annotations
import math
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import pathops

FONTS = "/workspace/lvc-launch-six/fonts"
NAVY = "#142B40"; OXBLOOD = "#852E34"; GOLD = "#C99B43"; GOLD_LIGHT = "#BD9143"
IVORY = "#E7D9BA"; IVORY_GARMENT = "#F4EEDF"
_F: dict[str, TTFont] = {}
TEXTS: list[str] = []   # every string placed, for proofing
CAPS: list[tuple[str, float]] = []  # (text, cap height px)
MODE = "outline"  # or "live"
LIVE = {
    "Inter-Regular": ("Inter", 400, "normal"), "Inter-Medium": ("Inter", 500, "normal"),
    "Inter-ExtraBold": ("Inter", 800, "normal"), "Inter-Black": ("Inter", 900, "normal"),
    "LibreBaskerville-Regular": ("Libre Baskerville", 400, "normal"),
    "LibreBaskerville-Bold": ("Libre Baskerville", 700, "normal"),
    "LibreBaskerville-Italic": ("Libre Baskerville", 400, "italic"),
    "BarlowCondensed-ExtraBold": ("Barlow Condensed", 800, "normal"),
}


def font(fam):
    if fam not in _F:
        _F[fam] = TTFont(f"{FONTS}/{fam}.ttf")
    return _F[fam]


def cap(fam, size):
    f = font(fam)
    return f["OS/2"].sCapHeight / f["head"].unitsPerEm * size


def _layout(text, fam, size, ls):
    f = font(fam); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    sc = size / f["head"].unitsPerEm
    out = []; x = 0.0
    for i, ch in enumerate(text):
        name = cmap.get(ord(ch))
        if name is None:
            raise ValueError(f"missing glyph {ch!r} in {fam}")
        out.append((ch, gs[name], x))
        x += gs[name].width * sc + (ls if i < len(text) - 1 else 0)
    return out, x, sc, gs


def width(text, fam, size, ls=0):
    return _layout(text, fam, size, ls)[1]


def fit(text, fam, maxw, ls=0):
    return maxw / width(text, fam, 1000, 0) * 1000 if ls == 0 else \
        (maxw - ls * (len(text) - 1)) / width(text, fam, 1000, 0) * 1000


def _start(x, w, anchor):
    return x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)


def T(text, fam, size, x, y, fill, ls=0, anchor="middle"):
    """Outlined text as one SVG path; records string for proofing."""
    TEXTS.append(text); CAPS.append((text, cap(fam, size)))
    lay, w, sc, gs = _layout(text, fam, size, ls)
    x0 = _start(x, w, anchor)
    if MODE == "live":
        f, wt, st = LIVE[fam]
        return (f'<text x="{x0:.1f}" y="{y:.1f}" font-family="{f}" font-weight="{wt}" font-style="{st}" '
                f'font-size="{size:.2f}" letter-spacing="{ls}" fill="{fill}">{escape(text)}</text>')
    pen = SVGPathPen(gs)
    for ch, g, gx in lay:
        if ch != " ":
            g.draw(TransformPen(pen, Transform(sc, 0, 0, -sc, x0 + gx, y)))
    return (f'<path data-text="{escape(text, {chr(34): "&quot;"})}" data-font="{fam}" '
            f'fill="{fill}" d="{pen.getCommands()}"/>')


def text_pathops(text, fam, size, x, y, ls=0, anchor="middle"):
    lay, w, sc, gs = _layout(text, fam, size, ls)
    x0 = _start(x, w, anchor)
    p = pathops.Path()
    pen = p.getPen()
    for ch, g, gx in lay:
        if ch != " ":
            g.draw(TransformPen(pen, Transform(sc, 0, 0, -sc, x0 + gx, y)))
    return pathops.simplify(p, fix_winding=True)


def poly_path(pts):
    p = pathops.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close(); return p


def rect_path(x, y, w, h):
    return poly_path([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def circle_path(cx, cy, r):
    k = 0.5522847498 * r; p = pathops.Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close(); return p


def diff(a, b):
    return pathops.op(a, b, pathops.PathOp.DIFFERENCE)


def union(a, b):
    return pathops.op(a, b, pathops.PathOp.UNION)


def to_d(p):
    pen = SVGPathPen(None); p.draw(pen); return pen.getCommands()


def knockout(block, text, fam, size, cx, baseline, fill, ls=0, extra_holes=None, id="knockout"):
    """Solid block minus text: a true hole, no masks."""
    TEXTS.append(text); CAPS.append((text, cap(fam, size)))
    t = text_pathops(text, fam, size, cx, baseline, ls)
    res = diff(block, t)
    if extra_holes is not None:
        res = diff(res, extra_holes)
    src = ""
    if MODE == "live":
        f, wt, st = LIVE[fam]; w = width(text, fam, size, ls)
        src = (f'<text id="{id}-source" display="none" x="{cx - w / 2:.1f}" y="{baseline:.1f}" font-family="{f}" '
               f'font-weight="{wt}" font-size="{size:.2f}" letter-spacing="{ls}">{escape(text)}</text>')
    return src + (f'<path id="{id}" data-text="{escape(text)}" data-font="{fam}" '
            f'fill="{fill}" fill-rule="nonzero" d="{to_d(res)}"/>'), t


IMPRINT_SIZE, IMPRINT_LS = 94, 9


def frame(color, number):
    imprint = T(f"THE ROYAL HOUSE OF ENGAGEMENT · NO. {number}",
                "LibreBaskerville-Regular", IMPRINT_SIZE, 2250, 4850, color, ls=IMPRINT_LS)
    return f'''<g id="house-frame">
<g fill="none" stroke="{color}">
<rect x="250" y="400" width="4000" height="4650" stroke-width="34"/>
<rect x="335" y="485" width="3830" height="4480" stroke-width="11"/>
</g>
<g fill="{color}">
<path d="M250 305l95 95-95 95-95-95z"/><path d="M4250 305l95 95-95 95-95-95z"/>
<path d="M250 4955l95 95-95 95-95-95z"/><path d="M4250 4955l95 95-95 95-95-95z"/>
<path d="M700 4800l60 60-60 60-60-60z"/><path d="M3800 4800l60 60-60 60-60-60z"/>
</g>
{imprint}
</g>'''


def doc(title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="4500" height="5400" '
            f'viewBox="0 0 4500 5400">\n<title>{escape(title)}</title>\n{body}\n</svg>\n')


def line(x1, y1, x2, y2, c, w, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" {extra}/>'


def signal_mark(x, y, s, bar_c, trace_c):
    """House of Signal: measured bars + ascending trace. (x,y)=bottom-left."""
    bw, gap = 0.15 * s, 0.09 * s
    out = []
    for i, h in enumerate([0.22, 0.36, 0.50, 0.64]):
        bx = x + i * (bw + gap)
        out.append(f'<rect x="{bx:.1f}" y="{y - h * s:.1f}" width="{bw:.1f}" height="{h * s:.1f}" fill="{bar_c}"/>')
    pts = [(x, y - 0.50 * s), (x + 0.30 * s, y - 0.64 * s), (x + 0.48 * s, y - 0.60 * s), (x + 0.90 * s, y - 1.00 * s)]
    ps = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    out.append(f'<polyline points="{ps}" fill="none" stroke="{trace_c}" stroke-width="{max(12, 0.05 * s):.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    ex, ey = pts[-1]
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{0.055 * s:.1f}" fill="{trace_c}"/>')
    return '<g id="signal-mark">' + "".join(out) + "</g>"


def scroll_mark(cx, top, s, feed_c, arrow_c):
    """House of Scroll: descending feed + down arrow."""
    out = []
    for i, w in enumerate([1.0, 0.74, 0.48]):
        out.append(f'<rect x="{cx - w * s / 2:.1f}" y="{top + i * 0.17 * s:.1f}" width="{w * s:.1f}" height="{0.075 * s:.1f}" fill="{feed_c}"/>')
    sw = max(14, 0.075 * s)
    a0, a1 = top + 0.56 * s, top + 1.05 * s
    out.append(f'<path d="M{cx:.1f} {a0:.1f}V{a1:.1f}M{cx - 0.2 * s:.1f} {a1 - 0.2 * s:.1f}L{cx:.1f} {a1:.1f}L{cx + 0.2 * s:.1f} {a1 - 0.2 * s:.1f}" fill="none" stroke="{arrow_c}" stroke-width="{sw:.1f}" stroke-linecap="square" stroke-linejoin="miter"/>')
    return '<g id="scroll-mark">' + "".join(out) + "</g>"
