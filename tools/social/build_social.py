#!/usr/bin/env python3
"""Build the social media kit: profile images, feed cards, and a captions-and-schedule CSV.

Run from the repository root:  python3 tools/social/build_social.py [--only PREFIX] [--no-render]

Needs Pillow and a Chrome/Chromium binary (set CHROME to override the macOS default). The cards use the
macOS system fonts Georgia and Snell Roundhand, as the website does. Output goes to design/social/.
Sources: docs/product/apparel-manifest.json, website/src/pages/{calendar,lineage}.astro,
docs/product/product-copy.md. Copy that lives nowhere else is in tools/social/content.py.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cards as C  # noqa: E402
import content as T  # noqa: E402

OUT = ROOT / "design" / "social"
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
GARMENT = {"ivory": "#efe6d2", "oxblood": "#7a2630", "navy": "#10263a", "black": "#1c1c1e"}
PRODUCT_GARMENT = {"validate": "ivory", "thought-leader": "navy", "doomscrolling": "oxblood", "content-creator": "ivory",
                   "authentic-self": "oxblood", "sent-regretted": "navy", "much-published": "navy", "order-blue-check": "black",
                   "y2k-the-almost": "oxblood", "saint-moth": "ivory"}
SLOT_DAYS = {0, 2, 4}  # Mon, Wed, Fri
START = date(2026, 11, 5)


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def typo(s):
    return s.replace("'", "’")


def load_sources():
    manifest = json.loads(read("docs/product/apparel-manifest.json"))
    cal = read("website/src/pages/calendar.astro")
    events = {}
    for m in re.finditer(r'"(\d\d-\d\d)": \{ year: "(\d+)", line: "(.*?)"(?:, latin: "(.*?)")? \}', cal):
        events[m.group(1)] = {"year": m.group(2), "line": m.group(3), "latin": m.group(4)}
    cdev = dict(re.findall(r'"(\d\d-\d\d)": "/assets/([^"]+)"', cal))
    lin = read("website/src/pages/lineage.astro")
    details = {m.group(1): {"motto": m.group(2), "account": m.group(3)}
               for m in re.finditer(r'"([\w-]+)": \{ motto: "(.*?)", account: "(.*?)" \}', lin)}
    ldev = dict(re.findall(r'"([\w-]+)": "/assets/([^"]+)"', lin.split("const devices")[1]))
    copy = read("docs/product/product-copy.md").split("## Wave 2")[0]
    desc = {int(m.group(1)): m.group(2).replace("*", "") for m in re.finditer(r"^\| (\d\d) \| (.*) \|$", copy, re.M)}
    return manifest, events, cdev, details, ldev, desc


HOLD_BLUE_CHECK = "HOLD: the Blue Check device still needs a rights review (docs/brand/IMAGERY_PRODUCTION_LOG.md)"


def notes_for(post_id, html):
    if "order-blue-check" in post_id or "order-blue-check" in html or "A08" in post_id:
        return HOLD_BLUE_CHECK
    if post_id.startswith("calendar-05-11"):
        return "REVIEW: names a real person (Kasparov); consider rewording for social"
    if post_id == "product-03-doomscrolling":
        return "REVIEW: the art for No. 03 is the weakest design; consider holding for the Duke of Doomscrolling redesign"
    if post_id.startswith("photo-") or post_id.startswith("plate-"):
        return "Concept image: keep the 'concept mockup' wording in the caption"
    return ""


def tags(kind, n=5):
    return " ".join((T.BASE_TAGS + T.KIND_TAGS.get(kind, []))[:n])


def build_posts():
    manifest, events, cdev, details, ldev, desc = load_sources()
    posts = []

    def add(pid, kind, html, caption, alt, pin=None, platforms="instagram,facebook"):
        posts.append({"id": pid, "kind": kind, "html": html, "caption": caption, "alt": alt, "pin": pin,
                      "platforms": platforms, "hashtags": tags(kind)})

    add("intro-premise", "intro", C.premise_card(), T.PREMISE_CAPTION,
        "Peacock-and-parrot arms of the Royal House of Engagement above the words: Official regalia for the attention economy.",
        platforms="instagram,facebook,linkedin")
    add("intro-status", "intro", C.status_card(), T.STATUS_CAPTION,
        "Notice reading: In early product development. The designs are working concepts, not products offered for sale.",
        platforms="instagram,facebook,linkedin")

    for key, (plate, title, cap, caption, alt) in T.PLATES.items():
        n = {"identity": 1, "collection": 2, "packaging": 3}[key]
        src = {"identity": "01-brand-identity-board.png", "collection": "02-apparel-collection.png", "packaging": "03-ceremonial-packaging.png"}[key]
        add(f"plate-{n}-{key}", "plate", C.plate_card(f"{C.ASSETS}/royal-house/{src}", plate, title, cap), caption, alt)

    for i, text in enumerate(manifest["constitution"]["principles"], 1):
        caption = f"{text}\n\n{T.PRINCIPLE_TAGS[i]}\n\nConstitutional principle No. {i} of the Royal House of Engagement."
        add(f"principle-{i:02d}", "principle", C.principle_card(i, text, dark=(i % 3 == 0)), caption,
            f"Card reading: {text}", platforms="instagram,facebook,linkedin")

    for h in manifest["houses"]:
        n = h["precedence"]
        caption = (f"{h['name']}. {h['standing']}\n\n“{h['contradiction']}”\n\n"
                   f"{h['institution']} · {h['latin']} ({h['line']})\n\nOne of the six Great Houses. Precedence changes with each reign.")
        add(f"house-{n:02d}-{h['id']}", "house",
            C.house_card(n, h["name"], h["standing"], h["contradiction"], h["institution"], h["latin"], h["line"], f"house-{h['id']}.svg"),
            caption, f"Badge of the {h['name']} above its description: {h['standing']}", platforms="instagram,facebook,linkedin")

    reigns = manifest["lineage"]
    for i, r in enumerate(reigns):
        d = details[r["id"]]
        present = i == len(reigns) - 1
        caption = f"{r['name']}, {r['period']}.\n\n{d['account']}\n\n{d['motto']}."
        add(f"lineage-{i + 1:02d}-{r['id']}", "lineage",
            C.lineage_card(ROMAN[i], r["name"], r["period"], d["motto"], d["account"], ldev[r["id"]], bool(r.get("disputed")), present),
            caption, f"Device of {r['name']}, reign {ROMAN[i]} of the Lineage of Engagement, {r['period']}.")

    for ev in manifest["observances"]:
        md = ev["monthDay"]
        mm, dd = (int(x) for x in md.split("-"))
        e = events[md]
        latin = f"\n\n{e['latin']}." if e["latin"] else ""
        caption = (f"From the Royal Calendar: today, {dd} {MONTHS[mm - 1]}, the {ev['name']}.\n\n{e['line']}{latin}\n\n"
                   f"Established {e['year']}.")
        slug = re.sub(r"[^a-z0-9]+", "-", ev["name"].lower()).strip("-")
        add(f"calendar-{md}-{slug}", "calendar",
            C.calendar_card(dd, MONTHS[mm - 1], ev["name"], e["year"], e["line"], e["latin"], cdev[md], dark=(md == "12-31")),
            caption, f"Card for the {ev['name']}, observed each {dd} {MONTHS[mm - 1]}: {e['line']}", pin=md)

    for p in manifest["launchProducts"]:
        n = p["position"]
        title = typo(p["primaryCopy"])
        art = Path(p["assets"]["frontArtDisplay"]).name
        garment = GARMENT[PRODUCT_GARMENT[p["id"]]]
        sub = p.get("latin") or p.get("originalCollection") or ""
        caption = f"{title}\n\n{typo(desc[n])}\n\nNo. {n:02d} in the founding collection. In development; not yet for sale."
        add(f"product-{n:02d}-{p['id']}", "product", C.product_card(n, title, sub, art, garment), caption,
            f"Front artwork for No. {n:02d}, {title.rstrip('.')}, shown on {'an' if PRODUCT_GARMENT[p['id']][0] in 'aeiou' else 'a'} {PRODUCT_GARMENT[p['id']]} garment panel.", platforms="instagram,facebook,linkedin")
        mock = ROOT / "website" / "public" / "assets" / f"shirt-{n:02d}-realm.png"
        if mock.exists():
            head, body = T.PHOTO_CAPTIONS[n]
            add(f"photo-{n:02d}-{p['id']}", "photo", C.photo_card(f"{C.ASSETS}/{mock.name}"), f"{head}\n\n{body}",
                f"Concept mockup of {title} on a wooden mannequin in an old-world study.")
    return posts


def render(job):
    html, out, w, h = job
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "card.html"
        f.write_text(html.replace("website/public", f"file://{ROOT}/website/public"), encoding="utf-8")
        png = Path(td) / "card.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--user-data-dir={td}/profile", f"--window-size={w},{h}", "--virtual-time-budget=2500",
                        f"--screenshot={png}", f"file://{f}"], capture_output=True, check=True)
        im = Image.open(png).convert("RGB")
        if im.size != (w, h):
            raise SystemExit(f"{out.name}: rendered {im.size}, expected {(w, h)}")
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.suffix == ".jpg":
            im.save(out, quality=92, subsampling=0, optimize=True)
        else:
            im.save(out, optimize=True)
    return out.name


SKIP_DATES = {date(2026, 12, 25)}


def is_held(post):
    n = notes_for(post["id"], post["html"])
    return n.startswith("HOLD") or n.startswith("REVIEW: the art")


def schedule(posts):
    """Assign suggested dates. Seed daily, then Mon/Wed/Fri slots; calendar cards pinned to their real dates.
    Held posts (rights review, weak art) are left unscheduled."""
    by_id = {p["id"]: p for p in posts}
    held = {p["id"] for p in posts if is_held(p)}
    dated = {}
    day = START
    for pid in T.SEED:
        dated[pid] = day
        day += timedelta(days=1)
    mon = [f"principle-{i:02d}" for i in range(2, 11)]
    wed = [p["id"] for p in posts if p["kind"] == "house"] + [p["id"] for p in posts if p["kind"] == "lineage" and p["id"] not in held]
    fri_order = ["photo-07", "product-07", "product-03", "photo-08", "product-08", "product-01", "photo-09", "product-09",
                 "product-02", "photo-10", "product-10", "product-04", "product-05", "product-06", "plate-2", "plate-3"]
    fri = [i for i in (next(p["id"] for p in posts if p["id"].startswith(k)) for k in fri_order) if i not in held]
    queues = {0: mon, 2: wed, 4: fri}
    pins = {p["pin"]: p["id"] for p in posts if p["pin"] and p["id"] not in held}
    d = day
    end = date(2027, 10, 31)
    while d <= end:
        if d in SKIP_DATES:
            d += timedelta(days=1)
            continue
        key = f"{d.month:02d}-{d.day:02d}"
        if key in pins and pins[key] not in dated:
            dated[pins[key]] = d
        elif d.weekday() in SLOT_DAYS and queues[d.weekday()]:
            dated[queues[d.weekday()].pop(0)] = d
        d += timedelta(days=1)
    return {pid: dated.get(pid) for pid in by_id}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="render only ids starting with this prefix")
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()

    posts = build_posts()
    dates = schedule(posts)
    feed = OUT / "feed"
    jobs = []
    if not a.only or "profile".startswith(a.only):
        prof = OUT / "profile"
        jobs += [(C.avatar(), prof / "avatar-1080.png", 1080, 1080),
                 (C.cover(1640, 624, scale=0.88), prof / "facebook-cover-1640x624.png", 1640, 624),
                 (C.cover(1584, 396, scale=0.7), prof / "linkedin-cover-1584x396.png", 1584, 396)]
    for p in posts:
        if not a.only or p["id"].startswith(a.only):
            jobs.append((p["html"], feed / f"{p['id']}.jpg", C.W, C.H))
    if not a.no_render:
        with ThreadPoolExecutor(max_workers=4) as ex:
            for name in ex.map(render, jobs):
                print("rendered", name)

    OUT.mkdir(parents=True, exist_ok=True)
    rows = sorted(posts, key=lambda p: (dates[p["id"]] or date(2999, 1, 1), p["id"]))
    with open(OUT / "posts.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["suggested_date", "id", "kind", "file", "platforms", "caption", "hashtags", "alt_text", "note"])
        for p in rows:
            dt = dates[p["id"]]
            w.writerow([dt.isoformat() if dt else ("hold" if is_held(p) else "unscheduled"), p["id"], p["kind"], f"feed/{p['id']}.jpg", p["platforms"],
                        p["caption"], p["hashtags"], p["alt"], notes_for(p["id"], p["html"])])
    print(f"{len(posts)} posts, {sum(1 for p in posts if dates[p['id']])} scheduled, {sum(1 for p in posts if is_held(p))} on hold -> {OUT / 'posts.csv'}")


if __name__ == "__main__":
    main()
