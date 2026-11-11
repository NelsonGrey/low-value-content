"""Mark's mixed picks (01-A, 02-A, 03-C, 04-B, 05-A, 06-A), finished for print.
Layouts follow the round-1 concept SVGs in /workspace/lvc-launch-six-concepts/svg/."""
import math
import lib
from lib import *

IB, IX, IM, IR = "Inter-Black", "Inter-ExtraBold", "Inter-Medium", "Inter-Regular"
LR, LB, LI, BC = "LibreBaskerville-Regular", "LibreBaskerville-Bold", "LibreBaskerville-Italic", "BarlowCondensed-ExtraBold"
N, O, G, I = NAVY, OXBLOOD, GOLD, IVORY
META = {}


def lsb(text, fam, size):
    f = font(fam); g = f.getBestCmap()[ord(text[0])]
    return f["hmtx"][g][1] * size / f["head"].unitsPerEm


def rrect(x, y, w, h, rx, stroke, sw, fill="none", extra=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')


# ------------------------------------------------------------------ 01-A progress bar
def s01():
    b = []; y = 0
    y += cap(LR, 120); b.append(T("PUBLIC REQUEST 0001", LR, 120, 2250, y, N, ls=46))
    s = fit("PLEASE VALIDATE ME", IX, 3300); c = cap(IX, s)
    y += 330 + c; b.append(T("PLEASE VALIDATE ME", IX, s, 2250, y, N))
    y += s * 1.12; b.append(T("ALGORITHMICALLY.", IX, s, 2250, y, N))
    # bar: bigger than comp (3200x250) -> 3300x330, fill stuck at ~10%
    W, H, sw, inset = 3300, 330, 34, 66
    top = y + 380
    b.append(rrect(2250 - W / 2, top, W, H, H / 2, N, sw))
    iw = W - 2 * inset; ih = H - 2 * inset
    fw = round(iw * 0.10)
    META["01"] = dict(bar=(W, H), fill_pct=round(100 * fw / iw, 1), saying_cap_px=round(c), number_cap_px=round(cap(LR, 120)), pending_cap_px=round(cap(IX, 150)))
    b.append(f'<rect x="{2250 - W / 2 + inset:.1f}" y="{top + inset:.1f}" width="{fw}" height="{ih}" rx="{ih / 2:.1f}" fill="{O}"/>')
    y = top + H + 300 + cap(IX, 150)
    b.append(T("REQUEST PENDING", IX, 150, 2250, y, N, ls=44))
    y += 170 + cap(LR, 104)
    b.append(T("ESTIMATED RECOGNITION · INDEFINITE", LR, 104, 2250, y, O, ls=26))
    return b


# ------------------------------------------------------------------ 02-A door plaque
def s02():
    b = []; y = 0
    y += cap(IM, 100); b.append(T("BY ALGORITHMIC APPOINTMENT", IM, 100, 2250, y, G, ls=38))
    x0, w = 650, 3200
    s = fit("THOUGHT", BC, 2500); c = cap(BC, s)
    ic = cap(LI, 180)
    inner_pad = 270
    h = 2 * inner_pad + 2 * c + 130 + 230 + ic + 70
    y0 = y + 200
    b.append(rrect(x0, y0, w, h, 0, G, 40))                    # outer plate rule
    b.append(rrect(x0 + 75, y0 + 75, w - 150, h - 150, 0, G, 16))  # inner rule (was 12)
    for sx in (x0 + 180, x0 + w - 180):
        for sy in (y0 + 180, y0 + h - 180):
            b.append(f'<circle cx="{sx}" cy="{sy:.1f}" r="40" fill="{G}"/>')
    t = y0 + inner_pad
    b.append(T("THOUGHT", BC, s, 2250, t + c, I))
    b.append(T("LEADER.", BC, s, 2250, t + 2 * c + 130, I))
    b.append(T("No thoughts required.", LI, 180, 2250, t + 2 * c + 130 + 230 + ic, G))
    META["02"] = dict(plaque=(w, round(h)), outer_rule_px=40, inner_rule_px=16, screw_d_px=80)
    b.append(T("OFFICIAL COURT APPOINTMENT · HONORARY", IM, 100, 2250, y0 + h + 220 + cap(IM, 100), I, ls=30))
    return b


# ------------------------------------------------------------------ 03-C field dispatch
NAME3 = "ROYAL INSTITUTE OF DIGITAL INQUIRY"


def s03():
    L, R = 640, 3860
    b = [rrect(L, 0, R - L, 300, 0, G, 14), f'<rect x="{L}" y="0" width="110" height="300" fill="{G}"/>']
    s = fit(NAME3, IX, R - L - 110 - 240, ls=24)
    b.append(T(NAME3, IX, s, L + 110 + 120, 150 + cap(IX, s) / 2, G, ls=24, anchor="start"))
    y = 385; b.append(line(L, y, R, y, G, 30))
    y += 15 + 300 + cap(LI, 215)
    b.append(T("I'm not doomscrolling.", LI, 215, L, y, I, anchor="start"))
    y += 120 + 230
    b.append(line(L, y - cap(IM, 130) / 2, L + 250, y - cap(IM, 130) / 2, G, 14))
    b.append(T("I'M DOING", IM, 130, L + 310, y, G, ls=44, anchor="start"))
    s2 = fit("RESEARCH.", BC, R - L); c = cap(BC, s2)
    y += 180 + c
    b.append(T("MARKET", BC, s2, L - lsb("MARKET", BC, s2), y, I, anchor="start"))
    y += s2 * 0.9
    b.append(T("RESEARCH.", BC, s2, L - lsb("RESEARCH.", BC, s2), y, I, anchor="start"))
    y += 230; b.append(line(L, y, R, y, G, 12))
    # lower third: enlarged House of Scroll charge (feed + arrow) beside a two-line footer
    ms = 620
    top = y + 190
    b.append(scroll_mark(L + ms / 2, top, ms, I, G))
    fs = 140; fc = cap(IM, fs)
    fx = L + ms + 230
    mid = top + 1.05 * ms / 2
    b.append(T("HOUSE OF SCROLL ·", IM, fs, fx, mid - 75, G, ls=34, anchor="start"))
    b.append(T("FIELD WORK CONTINUES", IM, fs, fx, mid + 75 + fc, G, ls=34, anchor="start"))
    b.append(line(fx, top, fx, top, G, 0))  # no-op anchor
    META["03"] = dict(scroll_mark_px=(ms, round(1.05 * ms)), footer_right_edge=round(fx + width("FIELD WORK CONTINUES", IM, fs, 34)))
    return [e for e in b if 'stroke-width="0"' not in e]


# ------------------------------------------------------------------ 04-B editor's marks
V4 = ["Uniqueness questionable.", "Monetization inconsistent.", "Visibility unreported."]


def s04():
    s = fit("CREATOR.", LB, 2900); c = cap(LB, s)
    x0 = 650
    b = [T("CONTENT", LB, s, x0 - lsb("C", LB, s), c, N, anchor="start"),
         T("CREATOR.", LB, s, x0 - lsb("C", LB, s), 2 * c + 420, N, anchor="start")]
    wc = width("CREATOR.", LB, s)
    ecx, ecy = x0 + wc / 2, c + 420 + c / 2
    pw, ph = wc + 200, c + 220
    b.append(f'<rect x="{ecx - pw / 2:.0f}" y="{ecy - ph / 2:.0f}" width="{pw:.0f}" height="{ph:.0f}" rx="{ph / 2:.0f}" '
             f'fill="none" stroke="{O}" stroke-width="18" transform="rotate(-1.5 {ecx:.0f} {ecy:.0f})"/>')
    xs = [980, 1180, 1380]
    ns = min((3880 - x) / width(v, LI, 1000) * 1000 for x, v in zip(xs, V4))
    ns = min(ns, 250)
    nc = cap(LI, ns)
    META["04"] = dict(verdict_size=round(ns, 1), verdict_cap_px=round(nc), title_cap_px=round(c), comp_verdict_size=175)
    y = 2 * c + 420 + 150 + 560
    lead = ns * 1.95
    k = ns / 175  # scale marks with the type
    sw = 18
    for i, v in enumerate(V4):
        bl = y + i * lead; tx = xs[i]
        b.append(T(v, LI, ns, tx, bl, O, anchor="start"))
        mx, my = tx - 230 * k, bl - nc / 2
        if i == 0:
            b.append(f'<path d="M{mx - 60 * k:.1f} {my + 60 * k:.1f}L{mx:.1f} {my - 70 * k:.1f}L{mx + 60 * k:.1f} {my + 60 * k:.1f}" fill="none" stroke="{O}" stroke-width="{sw}" stroke-linejoin="miter"/>')
        elif i == 1:
            b.append(line(mx - 25 * k, my - 75 * k, mx - 25 * k, my + 75 * k, O, sw) + line(mx + 25 * k, my - 75 * k, mx + 25 * k, my + 75 * k, O, sw))
        else:
            b.append(f'<path d="M{mx - 70 * k:.1f} {my + 60 * k:.1f}C{mx - 70 * k:.1f} {my - 90 * k:.1f} {mx + 70 * k:.1f} {my - 90 * k:.1f} {mx + 70 * k:.1f} {my:.1f}C{mx + 70 * k:.1f} {my + 60 * k:.1f} {mx + 10 * k:.1f} {my + 80 * k:.1f} {mx - 20 * k:.1f} {my + 40 * k:.1f}" fill="none" stroke="{O}" stroke-width="{sw}" stroke-linecap="round"/>')
    b.append(line(560, y - nc - 140, 560, y + 2 * lead + 110, O, 14))
    return b


# ------------------------------------------------------------------ 05-A price tag
def s05():
    b = []; y = 0
    ts, tls = 150, 40
    y += cap(LR, ts); b.append(T("MY AUTHENTIC SELF IS", LR, ts, 2250, y, I, ls=tls))
    y += 110 + cap(LR, ts); b.append(T("CURRENTLY BEING", LR, ts, 2250, y, I, ls=tls))
    str_top = y + 120
    ty = str_top + 260               # tag top edge
    x0, x1, ch, th = 800, 3700, 450, 1600
    poly = [(x0, ty + ch), (x0 + ch, ty), (x1 - ch, ty), (x1, ty + ch), (x1, ty + th), (x0, ty + th)]
    hc = (2250, ty + 220); hr = 85
    tag = poly_path(poly)
    hole = circle_path(hc[0], hc[1], hr)
    s = fit("MONETIZED", IB, 2350, ls=20); c = cap(IB, s)
    body_mid = (ty + ch + ty + th) / 2
    bl = body_mid + c / 2
    d, t = knockout(tag, "MONETIZED", IB, s, 2250, bl, G, ls=20, extra_holes=hole)
    b.append(d)
    b.append(line(2250, str_top, 2250, hc[1], G, 16))   # string, runs into the hole
    META["05"] = dict(poly=poly, hole=(hc[0], hc[1], hr), text=t.bounds, size=s, ls=20, string=(2250, str_top, hc[1], 16))
    y = ty + th + 260
    b.append(line(1650, y, 2850, y, G, 12))
    fs = 104; fc = cap(IM, fs)
    y += 170 + fc; b.append(T("SPONSORSHIP SUBJECT TO TERMS", IM, fs, 2250, y, I, ls=24))
    y += 110 + fc; b.append(T("PERSONA MAY DIFFER FROM PERSON", IM, fs, 2250, y, I, ls=24))
    return b


# ------------------------------------------------------------------ 06-A giant times
CHAIN = "SENT · DELIVERED · READ · REGRETTED"


def s06():
    ms = 300
    b = [signal_mark(2250 - 0.9 * ms / 2, 1.0 * ms, ms, G, I)]
    S, A = 1150, 270
    LS, LLS = 210, 56   # labels: comp was 130
    y = 1.0 * ms + 200
    for lab, num, col in (("SENT", "2:14", I), ("REGRETTED", "2:15", G)):
        W = width(num, IX, S) + 70 + width("AM.", IX, A)
        x = 2250 - W / 2
        lx = x + lsb(num, IX, S) - lsb(lab, IM, LS)
        y += cap(IM, LS)
        b.append(T(lab, IM, LS, lx, y, col, ls=LLS, anchor="start"))
        y += 120 + cap(IX, S)
        b.append(T(num, IX, S, x, y, col, anchor="start"))
        b.append(T("AM.", IX, A, x + width(num, IX, S) + 70, y, col, anchor="start"))
        y += 300
    META["06"] = dict(numeral_cap_px=round(cap(IX, S)), label_cap_px=round(cap(IM, LS)), comp_label_cap_px=round(cap(IM, 130)))
    y += 20
    b.append(line(1500, y, 3000, y, G, 12))
    b.append(T(CHAIN, IM, 104, 2250, y + 200 + cap(IM, 104), I, ls=26))
    return b


SHIRTS = [
    ("01", "progress-bar", "Progress bar", "Please validate me algorithmically.", IVORY_GARMENT, (N, O), O, s01,
     ["PUBLIC REQUEST 0001", "PLEASE VALIDATE ME ALGORITHMICALLY.", "REQUEST PENDING", "ESTIMATED RECOGNITION · INDEFINITE"]),
    ("02", "door-plaque", "Door plaque", "Thought leader. No thoughts required.", NAVY, (I, G), G, s02,
     ["BY ALGORITHMIC APPOINTMENT", "THOUGHT LEADER.", "No thoughts required.", "OFFICIAL COURT APPOINTMENT · HONORARY"]),
    ("03", "field-dispatch", "Field dispatch", "I'm not doomscrolling. I'm doing market research.", OXBLOOD, (I, G), G, s03,
     [NAME3, "I'm not doomscrolling.", "I'M DOING", "MARKET RESEARCH.", "HOUSE OF SCROLL · FIELD WORK CONTINUES"]),
    ("04", "editors-marks", "Editor's marks", "Content creator.", IVORY_GARMENT, (N, O), O, s04, ["CONTENT CREATOR."] + V4),
    ("05", "price-tag", "Price tag", "My authentic self is currently being monetized.", OXBLOOD, (I, G), G, s05,
     ["MY AUTHENTIC SELF IS CURRENTLY BEING", "MONETIZED", "SPONSORSHIP SUBJECT TO TERMS", "PERSONA MAY DIFFER FROM PERSON"]),
    ("06", "giant-times", "Giant times", "Sent 2:14 AM. Regretted 2:15 AM.", NAVY, (I, G), G, s06,
     ["SENT 2:14 AM.", "REGRETTED", "2:15 AM.", CHAIN]),
]
