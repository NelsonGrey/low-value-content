#!/usr/bin/env python3
"""Static checks for the website and repo config. Standard library only.

Checks every HTML page under website/dist and website/coming-soon for: <html lang>,
<title>, viewport, meta description (not on 404 pages), and that local links, scripts,
stylesheets, and images resolve to files. Also validates the JSON config files.
Run from the repository root: python3 scripts/check-site.py
"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITES = [ROOT / "website" / "dist", ROOT / "website" / "coming-soon", ROOT / "website" / "royal" / "dist"]
JSON_FILES = [".firebaserc", *(p.name for p in ROOT.glob("firebase*.json"))]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = False
        self.title = False
        self.viewport = False
        self.description = False
        self.refs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html" and a.get("lang"):
            self.lang = True
        if tag == "title":
            self.title = True
        if tag == "meta":
            if a.get("name") == "viewport":
                self.viewport = True
            if a.get("name") == "description" and a.get("content"):
                self.description = True
        for attr in ("href", "src"):
            if tag in ("a", "link", "script", "img", "source") and a.get(attr):
                self.refs.append(a[attr])


def local_target(site: Path, page: Path, ref: str):
    parsed = urlparse(ref)
    if parsed.scheme or parsed.netloc or ref.startswith(("#", "mailto:", "tel:", "data:")):
        return None
    path = parsed.path
    if not path:
        return None
    base = site if path.startswith("/") else page.parent
    target = (base / path.lstrip("/")).resolve()
    if target.is_dir():
        target = target / "index.html"
    return target


def main() -> int:
    errors = []
    pages = 0
    for site in SITES:
        if not site.is_dir():
            continue
        for page in sorted(site.rglob("*.html")):
            pages += 1
            rel = page.relative_to(ROOT)
            parser = Page()
            parser.feed(page.read_text(encoding="utf-8"))
            for ok, label in ((parser.lang, "<html lang>"), (parser.title, "<title>"), (parser.viewport, "viewport meta")):
                if not ok:
                    errors.append(f"{rel}: missing {label}")
            if page.name != "404.html" and not parser.description:
                errors.append(f"{rel}: missing meta description")
            for ref in parser.refs:
                target = local_target(site, page, ref)
                if target is None:
                    continue
                if not target.exists():
                    # clean URLs: /about resolves to about.html
                    clean = target.with_suffix(".html") if not target.suffix else target
                    if not clean.exists():
                        errors.append(f"{rel}: broken local reference {ref!r}")
    for name in JSON_FILES:
        path = ROOT / name
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{name}: invalid JSON ({exc})")
    if pages == 0:
        errors.append("no HTML pages found under website/")
    for line in errors:
        print(f"ERROR {line}")
    print(f"checked {pages} pages, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
