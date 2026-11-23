// Behavior test for the pinned-header page shell: header stays put, only #page-scroll scrolls, keyboard and
// anchors work, sticky panels stick, Back restores scroll, the mobile menu opens. Uses real (classic) scrollbars.
import http from "node:http"; import fs from "node:fs"; import path from "node:path";
import { fileURLToPath } from "node:url"; import { chromium } from "playwright-core";

const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../website/dist");
const T = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".woff2": "font/woff2" };
const srv = http.createServer((q, s) => { let p = decodeURIComponent(new URL(q.url, "http://x").pathname); let f = path.join(dist, p);
  if (!fs.existsSync(f) && fs.existsSync(f + ".html")) f += ".html";
  if (!f.startsWith(dist) || !fs.existsSync(f)) { s.writeHead(404); return s.end(); }
  s.writeHead(200, { "Content-Type": T[path.extname(f)] || "application/octet-stream" }); fs.createReadStream(f).pipe(s); });
await new Promise((r) => srv.listen(0, r));
const base = `http://localhost:${srv.address().port}`;
const browser = await chromium.launch({ channel: "chrome", ignoreDefaultArgs: ["--hide-scrollbars"] });
let failures = 0;
const check = (name, ok, got) => { console.log(`${ok ? "PASS" : "FAIL"}  ${name}${ok ? "" : "  got: " + JSON.stringify(got)}`); if (!ok) failures++; };
const open = async (w, h, url) => { const page = await (await browser.newContext({ viewport: { width: w, height: h } })).newPage(); await page.goto(base + url, { waitUntil: "load" }); return page; };
const state = (page) => page.evaluate(() => { const s = document.getElementById("page-scroll"); const h = document.querySelector(".site-header").getBoundingClientRect();
  return { docScroll: window.scrollY, top: s?.scrollTop ?? null, headerTop: h.top, headerBottom: Math.round(h.bottom), headerLeftLogo: Math.round(document.querySelector(".brand-lockup").getBoundingClientRect().left * 10) / 10, canScroll: s ? s.scrollHeight > s.clientHeight : null }; });

// 1. Header pinned, only the body scrolls (desktop)
let page = await open(1440, 800, "/shop.html");
let a = await state(page);
await page.mouse.move(700, 500); await page.mouse.wheel(0, 1200); await page.waitForTimeout(900);
let b = await state(page);
check("desktop: document itself does not scroll", b.docScroll === 0, b);
check("desktop: body scrolled", b.top > 500, b);
check("desktop: header stays at the top", b.headerTop === 0 && b.headerBottom === a.headerBottom, { a, b });
check("desktop: header content does not move sideways", b.headerLeftLogo === a.headerLeftLogo, { a: a.headerLeftLogo, b: b.headerLeftLogo });

// 2. Keyboard scrolling works without clicking first
page = await open(1440, 800, "/terms.html");
await page.keyboard.press("PageDown"); await page.waitForTimeout(700);
let k = await state(page);
check("desktop: Page Down scrolls the body from a fresh load", k.top > 0 || k.canScroll === false, k);
page = await open(1440, 600, "/shop.html");
await page.keyboard.press("End"); await page.waitForTimeout(1500);
k = await state(page);
const atEnd = await page.evaluate(() => { const s = document.getElementById("page-scroll"); return s.scrollHeight - s.clientHeight - s.scrollTop < 3; });
check("desktop: End key reaches the footer", atEnd, k);

// 3. Anchor links scroll the body (social page uses #instagram etc.)
page = await open(1440, 700, "/social.html");
const hasAnchor = await page.evaluate(() => !!document.getElementById("linkedin"));
if (hasAnchor) {
  await page.evaluate(() => { location.hash = "#linkedin"; }); await page.waitForTimeout(900);
  const an = await state(page);
  check("desktop: #anchor scrolls the body, header stays", an.top > 0 && an.headerTop === 0 && an.docScroll === 0, an);
}

// 4. Back restores the body's scroll position
page = await open(1440, 700, "/shop.html");
await page.mouse.move(700, 400); await page.mouse.wheel(0, 900); await page.waitForTimeout(900);
const before = (await state(page)).top;
await page.click('a[href="/cart.html"]'); await page.waitForURL(/cart/);
await page.goBack(); await page.waitForURL(/shop/); await page.waitForTimeout(900);
const after = (await state(page)).top;
check("desktop: Back restores scroll position", Math.abs(after - before) < 5 && before > 0, { before, after });

// 5. Sticky panels still stick
page = await open(1440, 800, "/products/validate.html");
await page.mouse.move(1000, 500); await page.mouse.wheel(0, 600); await page.waitForTimeout(900);
const vis = await page.evaluate(() => { const v = document.querySelector(".product-visual").getBoundingClientRect(); const h = document.querySelector(".site-header").getBoundingClientRect(); return { visTop: Math.round(v.top), headerBottom: Math.round(h.bottom), visBottom: Math.round(v.bottom), vh: innerHeight }; });
check("product page: artwork panel stays pinned under the header", vis.visTop === vis.headerBottom && vis.visBottom <= vis.vh + 1, vis);
page = await open(1440, 800, "/realm/constitution.html");
await page.mouse.move(700, 500); await page.mouse.wheel(0, 900); await page.waitForTimeout(900);
const sh = await page.evaluate(() => { const e = document.querySelector(".hierarchy .section-heading"); const h = document.querySelector(".site-header").getBoundingClientRect(); return e ? { top: Math.round(e.getBoundingClientRect().top), headerBottom: Math.round(h.bottom) } : null; });
check("constitution: sticky heading sits just under the header", sh && sh.top >= sh.headerBottom && sh.top < sh.headerBottom + 80, sh);

// 6. Mobile: header pinned by sticky positioning, document scroll, menu opens over content
page = await open(390, 800, "/shop.html");
await page.evaluate(() => window.scrollTo(0, 900)); await page.waitForTimeout(400);
const m = await page.evaluate(() => ({ y: window.scrollY, headerTop: Math.round(document.querySelector(".site-header").getBoundingClientRect().top), shell: getComputedStyle(document.body).overflow }));
check("mobile: page scrolls normally and the header stays pinned", m.y > 500 && m.headerTop === 0 && m.shell === "visible", m);
await page.click(".menu-button"); await page.waitForTimeout(300);
const menu = await page.evaluate(() => { const n = document.querySelector("#site-navigation"); const r = n.getBoundingClientRect(); return { open: n.classList.contains("open"), visible: r.height > 100, top: Math.round(r.top) }; });
check("mobile: menu opens under the pinned header", menu.open && menu.visible, menu);

// 7. Print keeps the whole document
page = await open(1440, 800, "/terms.html");
await page.emulateMedia({ media: "print" });
const pr = await page.evaluate(() => ({ overflow: getComputedStyle(document.body).overflow, scrollerOverflow: getComputedStyle(document.getElementById("page-scroll")).overflowY, h: document.documentElement.scrollHeight, vh: innerHeight }));
check("print: nothing is clipped by the scroll shell", pr.overflow === "visible" && pr.scrollerOverflow === "visible" && pr.h > pr.vh, pr);

await browser.close(); srv.close();
console.log(failures ? `${failures} FAILED` : "all passed"); process.exit(failures ? 1 : 0);
