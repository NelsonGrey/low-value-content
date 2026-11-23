// Measures header/content/footer left edges on a short page (cart) and a long one (shop), with real scrollbars.
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
let worst = 0;
for (const width of [1920, 1440, 1280, 1000, 390]) {
  const rows = {};
  for (const pg of ["cart", "shop", "terms", "index"]) {
    const page = await (await browser.newContext({ viewport: { width, height: Number(process.env.VH || 900) } })).newPage();
    await page.goto(`${base}/${pg}.html`, { waitUntil: "load" });
    rows[pg] = await page.evaluate(() => {
      const x = (sel) => { const e = document.querySelector(sel); return e ? Math.round(e.getBoundingClientRect().left * 10) / 10 : null; };
      const h = document.querySelector(".brand-lockup img, .brand-lockup")?.getBoundingClientRect().left;
      const c = (document.querySelector("main h1, main .eyebrow")?.getBoundingClientRect().left) ?? null;
      const f = document.querySelector(".footer-house")?.getBoundingClientRect().left ?? null;
      const nl = document.querySelector('.site-header nav a:last-child'); const nr = nl && nl.offsetParent ? Math.round(nl.getBoundingClientRect().right * 10) / 10 : null;
      return { navRight: nr, logo: Math.round(h * 10) / 10, content: c && Math.round(c * 10) / 10, footer: f && Math.round(f * 10) / 10, scrollbar: window.innerWidth - document.documentElement.clientWidth };
    });
  }
  const logos = Object.values(rows).map((r) => r.logo);
  const navs = Object.values(rows).map((r) => r.navRight).filter((v) => v != null);
  const navSpread = navs.length ? Math.max(...navs) - Math.min(...navs) : 0;
  const misalign = Math.max(...Object.values(rows).map((r) => (r.content == null ? 0 : Math.abs(r.logo - r.content))));
  const spread = Math.max(Math.max(...logos) - Math.min(...logos), navSpread, misalign);
  worst = Math.max(worst, spread);
  console.log(`${width}px  logo x by page: ` + Object.entries(rows).map(([k, r]) => `${k}=${r.logo}(sb ${r.scrollbar})`).join("  ") + `   navRight=` + Object.entries(rows).map(([k, r]) => `${k}:${r.navRight}`).join(" ") + `  navSpread=${navSpread}px logo-vs-content=${misalign}px   content(cart)=${rows.cart.content} footer(cart)=${rows.cart.footer}`);
}
console.log(worst > 0.5 ? `HEADER SHIFTS (worst ${worst}px)` : "header stable across pages");
await browser.close(); srv.close(); process.exit(worst > 0.5 ? 1 : 0);
