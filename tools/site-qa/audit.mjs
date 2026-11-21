// Audits the built site (website/dist) in a real Chrome: full-page screenshots at three widths,
// axe accessibility violations, horizontal overflow on phones, and the 1280px layout rule.
// Usage: npm run build --prefix website && cd tools/site-qa && npm install && npm run audit [-- --pages index,shop]
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright-core";
import AxeBuilder from "@axe-core/playwright";

const here = path.dirname(fileURLToPath(import.meta.url));
const dist = path.resolve(here, "../../website/dist");
const out = path.join(here, "out");
fs.mkdirSync(out, { recursive: true });
const arg = process.argv.find((a) => a.startsWith("--pages="))?.split("=")[1];
const PAGES = (arg ? arg.split(",") : ["index", "shop", "products/validate", "products/sent-regretted", "cart", "realm", "realm/constitution", "realm/houses", "realm/peerage", "lineage", "calendar", "about", "support", "terms"]);
const VIEWPORTS = [{ name: "desktop-1920", width: 1920, height: 1080 }, { name: "laptop-1280", width: 1280, height: 800 }, { name: "small-600", width: 600, height: 900 }, { name: "tablet-820", width: 820, height: 1100 }, { name: "phone-390", width: 390, height: 844 }];
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".ico": "image/x-icon" };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  if (p.endsWith("/")) p += "index.html";
  let file = path.join(dist, p);
  if (!fs.existsSync(file) && fs.existsSync(file + ".html")) file += ".html";
  if (!file.startsWith(dist) || !fs.existsSync(file)) { res.writeHead(404); return res.end("not found"); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(0, r));
const base = `http://localhost:${server.address().port}`;

const browser = await chromium.launch({ channel: "chrome" });
const report = [];
for (const page_ of PAGES) {
  const entry = { page: page_, axe: [], overflow: [], layout: [], scrollers: [], wraps: [] };
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await ctx.newPage();
    await page.goto(`${base}/${page_}.html`, { waitUntil: "networkidle" });
    await page.screenshot({ path: path.join(out, `${page_.replaceAll("/", "_")}-${vp.name}.png`), fullPage: true });
    if (vp.name === "desktop-1920") {
      const results = await new AxeBuilder({ page }).analyze();
      entry.axe = results.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, help: v.help }));
      // 1280px layout rule: outside header/footer, no element wider than ~1300px may paint a background.
      entry.layout = await page.evaluate(() => {
        const bad = [];
        for (const el of document.querySelectorAll("body *")) {
          if (el.closest("header, footer, nav")) continue;
          const r = el.getBoundingClientRect();
          if (r.width < 1320) continue;
          const cs = getComputedStyle(el);
          const paints = (cs.backgroundColor !== "rgba(0, 0, 0, 0)" && cs.backgroundColor !== "transparent") || cs.backgroundImage !== "none";
          if (paints) bad.push(`${el.tagName.toLowerCase()}.${(el.className || "").toString().split(" ")[0]} ${Math.round(r.width)}px`);
        }
        return bad.slice(0, 12);
      });
    }
    // Inner horizontal scrollers (a strip that needs a sideways roll) at every width.
    const scrollers = await page.evaluate(() => [...document.querySelectorAll("body *")].filter((el) => { const cs = getComputedStyle(el); return /(auto|scroll)/.test(cs.overflowX) && el.scrollWidth > el.clientWidth + 1; }).slice(0, 6).map((el) => `${el.tagName.toLowerCase()}.${(el.className || "").toString().split(" ")[0]}`));
    for (const sc of scrollers) entry.scrollers.push(`${vp.name}: ${sc}`);
    // Names that must stay on one line (e.g. "House of Influence"), and page-level sideways overflow at every width.
    const wraps = await page.evaluate(() => { const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) { const m = n.textContent.match(/House of (Prompt|Scroll|Influence|Signal|Spam|Buffer)/); if (!m) continue; const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length); const tops = new Set([...r.getClientRects()].map((q) => Math.round(q.top))); if (tops.size > 1) out.push(m[0]); } return out; });
    for (const x of wraps) entry.wraps.push(`${vp.name}: ${x}`);
    const over = await page.evaluate(() => (document.documentElement.scrollWidth > window.innerWidth ? `scrollWidth ${document.documentElement.scrollWidth} > ${window.innerWidth}` : null));
    if (over) entry.overflow.push(`${vp.name}: ${over}`);
    await ctx.close();
  }
  report.push(entry);
  console.log(`${page_}: axe ${entry.axe.length} rules, layout-rule ${entry.layout.length}, overflow ${entry.overflow.length}, inner scrollers ${entry.scrollers.length}, wrapped names ${entry.wraps.length}`);
}
await browser.close();
server.close();
fs.writeFileSync(path.join(out, "report.json"), JSON.stringify(report, null, 2));
console.log(`\nWrote ${path.relative(process.cwd(), out)}/report.json and screenshots`);
