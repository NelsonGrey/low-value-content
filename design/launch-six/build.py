#!/usr/bin/env python3
"""Rebuild the Low Value Content launch six (chosen C concepts) print files.
Run: /workspace/lvc-launch-six/.venv/bin/python /workspace/lvc-launch-six-print-mix/build.py
"""
import io, re, json
from pathlib import Path
import numpy as np, cairosvg
from PIL import Image, ImageCms, ImageDraw, ImageFont, ImageFilter
import lib, chosen

ROOT = Path(__file__).resolve().parent
FONTDIR = lib.FONTS


def raster(svg, w=4500, h=5400):
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=w, output_height=h, background_color="rgba(0,0,0,0)")
    return np.array(Image.open(io.BytesIO(png)).convert("RGBA"))


def hexrgb(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)])


def quantize(arr, inks):
    """Hard screen-print edges: alpha 0/255 only, every opaque pixel snapped to one of the two inks."""
    a = arr[:, :, 3] >= 128
    pal = np.stack([hexrgb(c) for c in inks])
    rgb = arr[:, :, :3].astype(int)
    d = ((rgb[:, :, None, :] - pal[None, None, :, :]) ** 2).sum(-1)
    idx = d.argmin(-1)
    out = np.zeros_like(arr)
    out[:, :, :3] = pal[idx]
    out[:, :, 3] = a * 255
    out[~a] = 0
    return out


SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
FONT_CSS = "\n".join(
    f'@font-face {{ font-family: "{fam}"; font-weight: {wt}; font-style: {st}; src: url("file://{FONTDIR}/{key}.ttf"); }}'
    for key, (fam, wt, st) in lib.LIVE.items())


def editable_doc(title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="4500" height="5400" viewBox="0 0 4500 5400">\n'
            f'<title>{title}</title>\n<desc>EDITABLE master: live type. Fonts (static instances) in {FONTDIR}: '
            f'Inter Regular/Medium/ExtraBold/Black, Libre Baskerville Regular/Bold/Italic, Barlow Condensed ExtraBold. '
            f'Knockouts are outlined compound paths (a hidden source text is kept beside each). '
            f'Print from the outlined file in ../print/.</desc>\n<style>\n{FONT_CSS}\n</style>\n{body}\n</svg>\n')


report = {}
for nn, slug, disp, title, garment, inks, framec, fn, req in chosen.SHIRTS:
    name = f"{nn}-{slug}"
    # --- outlined print master
    lib.MODE = "outline"; lib.TEXTS.clear(); lib.CAPS.clear()
    body = "\n".join(fn())
    probe = raster(lib.doc("p", body), 450, 540)[:, :, 3]
    ys, xs = np.nonzero(probe > 10)
    dy = round((620 + 4650) / 2 - (ys.min() + ys.max()) * 5)
    texts = list(lib.TEXTS)
    frame = lib.frame(framec, nn)
    imprint = lib.TEXTS[-1]
    caps = list(lib.CAPS)
    svg = lib.doc(f"No. {nn} — {title} (print, outlined)",
                  f'<g id="content" transform="translate(0 {dy})">\n{body}\n</g>\n{frame}')
    (ROOT / "print" / f"{name}.svg").write_text(svg, encoding="utf-8")
    # --- editable master (same geometry, live type)
    lib.MODE = "live"; lib.TEXTS.clear()
    ebody = "\n".join(fn()); eframe = lib.frame(framec, nn)
    (ROOT / "editable" / f"{name}.svg").write_text(editable_doc(f"No. {nn} — {title} (editable)",
        f'<g id="content" transform="translate(0 {dy})">\n{ebody}\n</g>\n{eframe}'), encoding="utf-8")
    lib.MODE = "outline"
    # --- PNG
    raw = raster(svg)
    q = quantize(raw, inks)
    Image.fromarray(q, "RGBA").save(ROOT / "print" / f"{name}.png", dpi=(300, 300), icc_profile=SRGB, optimize=True)
    art = Image.fromarray(q, "RGBA")
    bg = Image.new("RGBA", art.size, tuple(hexrgb(garment)) + (255,))
    prev = Image.alpha_composite(bg, art).convert("RGB")
    prev.resize((1800, 2160), Image.LANCZOS).save(ROOT / "previews" / f"{name}.png")
    prev.resize((200, 240), Image.LANCZOS).save(ROOT / "check" / f"thumb-{name}.png")
    # --- checks
    joined = " ".join(texts)
    allowed = set(" ".join(req).split())
    hexes = set(c.upper() for c in re.findall(r"#[0-9A-Fa-f]{6}", svg))
    strokes = [float(v) for v in re.findall(r'stroke-width="([\d.]+)"', svg)]
    A = q[:, :, 3]; op = A == 255
    cols = {tuple(c) for c in np.unique(q[op][:, :3], axis=0)}
    yy, xx = np.nonzero(op)
    content = raw.copy()
    imp_w = lib.width(imprint, "LibreBaskerville-Regular", lib.IMPRINT_SIZE, lib.IMPRINT_LS)
    r = dict(dy=dy,
             missing=[x for x in req if x not in joined],
             extra_words=[w for w in joined.split() if w not in allowed],
             imprint=imprint, imprint_ok=imprint == f"THE ROYAL HOUSE OF ENGAGEMENT · NO. {nn}",
             imprint_clear_of_diamonds_px=round(min((2250 - imp_w / 2) - 760, 3740 - (2250 + imp_w / 2))),
             curly_quotes=any(ch in joined for ch in "\u2018\u2019\u02bc"),
             svg_colours=sorted(hexes), svg_colours_ok=hexes <= {c.upper() for c in inks},
             png_alpha_values=sorted(int(v) for v in np.unique(A)),
             png_colours=sorted("#%02X%02X%02X" % c for c in cols),
             min_stroke_px=min(strokes),
             min_cap_px=round(min(c for _, c in caps), 1),
             min_cap_text=min(caps, key=lambda t: t[1])[0],
             art_bbox=[int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())],
             editable_text_elements=ebody.count("<text"),
             )
    # content (excluding frame) must sit inside inner frame and above imprint
    cprobe = raster(lib.doc("c", f'<g transform="translate(0 {dy})">{body}</g>'))[:, :, 3]
    cy_, cx_ = np.nonzero(cprobe > 0)
    r["content_bbox"] = [int(cx_.min()), int(cy_.min()), int(cx_.max()), int(cy_.max())]
    r["content_inside_inner_frame"] = bool(cx_.min() > 335 + 100 and cx_.max() < 4165 - 100 and cy_.min() > 485 + 100 and cy_.max() < 4850 - 94 - 120)
    r["outer_3pct_clear"] = bool(xx.min() >= 135 and xx.max() <= 4365 and yy.min() >= 162 and yy.max() <= 5238)
    if nn in chosen.META and nn != "05":
        r.update(chosen.META[nn])
    if nn == "05":
        m = chosen.META["05"]
        tp = lib.text_pathops("MONETIZED", chosen.IB, m["size"], 2250, 0, m["ls"])
        offy = m["text"][3] - tp.bounds[3]
        def mask(d, extra=""):
            return raster(lib.doc("m", f'<g transform="translate(0 {dy})">{extra}<path d="{d}"/></g>'))[:, :, 3]
        tm = raster(lib.doc("t", f'<g transform="translate(0 {dy + offy})"><path d="{lib.to_d(tp)}"/></g>'))[:, :, 3]
        tagm = mask(lib.to_d(lib.poly_path(m["poly"])))
        hx, hy, hr = m["hole"]
        holem = mask(lib.to_d(lib.circle_path(hx, hy, hr)))
        sx, s0, s1, ssw = m["string"]
        strm = raster(lib.doc("s", f'<g transform="translate(0 {dy})">{lib.line(sx, s0, sx, s1, "#000", ssw)}</g>'))[:, :, 3]
        er = lambda a, n: np.array(Image.fromarray(((a >= 128) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(n))) > 0
        di = lambda a, n: np.array(Image.fromarray(((a > 0) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(n))) > 0
        glyph = tm >= 128; core = er(tm, 3)
        tag_in = er(tagm, 5)
        solid_zone = tag_in & ~di(tm, 5) & ~di(holem, 5) & ~di(strm, 3)
        edge_band = tag_in & ~er(tagm, 41) & ~di(holem, 5)        # 20-px band just inside the tag outline
        hole_open = er(holem, 5) & ~di(strm, 3)
        ty_, tx_ = np.nonzero(glyph)
        tag_y, tag_x = np.nonzero(tagm >= 128)
        # nearest distance from letters to tag outline (horizontal / vertical, plus chamfer via distance transform)
        from scipy.ndimage import distance_transform_edt as edt
        dist = edt(tagm >= 128)
        r["knockout"] = dict(
            method="gold tag polygon minus string-hole circle minus Inter Black MONETIZED outlines (skia-pathops DIFFERENCE); no SVG mask",
            letter_pixels=int(glyph.sum()), letter_pixels_transparent=int((A[glyph] == 0).sum()),
            letter_core_pixels=int(core.sum()), letter_core_transparent=int((A[core] == 0).sum()),
            tag_solid_pixels_checked=int(solid_zone.sum()),
            tag_solid_outside_letters_pct=round(100 * float((A[solid_zone] == 255).mean()), 4),
            tag_edge_band_pixels=int(edge_band.sum()), tag_edge_band_opaque_pct=round(100 * float((A[edge_band] == 255).mean()), 4),
            hole_open_pixels=int(hole_open.sum()), hole_open_transparent=int((A[hole_open] == 0).sum()),
            min_letter_to_tag_edge_px=round(float(dist[glyph].min()), 1),
            letter_margin_px=dict(left=int(tx_.min() - tag_x.min()), right=int(tag_x.max() - tx_.max()),
                                  top_to_tag_body=int(ty_.min() - (m["poly"][0][1] + dy)), bottom=int(tag_y.max() - ty_.max())),
        )
        (ROOT / "check" / "knockout.json").write_text(json.dumps(r["knockout"], indent=1))
    report[name] = r
    print(name, json.dumps({k: v for k, v in r.items() if k not in ("knockout",)}, ensure_ascii=False))
    if "knockout" in r: print("  knockout", r["knockout"])

(ROOT / "check" / "proof.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))

# --- contact sheet
F = lambda n, s: ImageFont.truetype(f"{FONTDIR}/{n}.ttf", s)
tw, th, gap, pad = 720, 864, 50, 80
W = pad * 2 + 3 * tw + 2 * gap; H = 190 + 2 * (th + 150) + 40
sheet = Image.new("RGB", (W, H), (226, 223, 216)); d = ImageDraw.Draw(sheet)
d.text((pad, 60), "Low Value Content · Holiday launch six · print artwork", font=F("Inter-ExtraBold", 50), fill=(30, 30, 30))
for i, (nn, slug, disp, title, *_r) in enumerate(chosen.SHIRTS):
    rr, cc = divmod(i, 3)
    x = pad + cc * (tw + gap); y = 190 + rr * (th + 150)
    sheet.paste(Image.open(ROOT / "previews" / f"{nn}-{slug}.png").resize((tw, th), Image.LANCZOS), (x, y))
    d.text((x, y + th + 22), f"No. {nn} — {disp}", font=F("Inter-Black", 40), fill=(30, 30, 30))
    d.text((x, y + th + 76), title, font=F("Inter-Medium", 28), fill=(70, 70, 70))
sheet.save(ROOT / "previews" / "launch-six-contact-sheet.png")
print("done")
