// Lighthouse (performance, accessibility, best practices, SEO) for the built site, mobile and desktop.
// Usage: cd tools/site-qa && npm run lighthouse [-- --pages=index,shop]
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import lighthouse from "lighthouse";
import { launch } from "chrome-launcher";

const here = path.dirname(fileURLToPath(import.meta.url));
const dist = path.resolve(here, "../../website/dist");
const out = path.join(here, "out");
fs.mkdirSync(out, { recursive: true });
const arg = process.argv.find((a) => a.startsWith("--pages="))?.split("=")[1];
const PAGES = arg ? arg.split(",") : ["index", "shop", "products/validate"];
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  if (p.endsWith("/")) p += "index.html";
  let file = path.join(dist, p);
  if (!fs.existsSync(file) && fs.existsSync(file + ".html")) file += ".html";
  if (!file.startsWith(dist) || !fs.existsSync(file)) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(0, r));
const base = `http://localhost:${server.address().port}`;
const chrome = await launch({ chromeFlags: ["--headless=new", "--no-sandbox"] });
const rows = [];
for (const page of PAGES) {
  for (const form of ["mobile", "desktop"]) {
    const res = await lighthouse(`${base}/${page}.html`, { port: chrome.port, output: "json", logLevel: "error", formFactor: form, screenEmulation: form === "desktop" ? { mobile: false, width: 1350, height: 940, deviceScaleFactor: 1, disabled: false } : undefined, throttlingMethod: "simulate" });
    const c = res.lhr.categories, a = res.lhr.audits;
    rows.push({ page, form, perf: Math.round(c.performance.score * 100), a11y: Math.round(c.accessibility.score * 100), bp: Math.round(c["best-practices"].score * 100), seo: Math.round(c.seo.score * 100), lcp: a["largest-contentful-paint"].displayValue, cls: a["cumulative-layout-shift"].displayValue, tbt: a["total-blocking-time"].displayValue, bytes: a["total-byte-weight"].displayValue });
    console.log(rows.at(-1));
  }
}
await chrome.kill();
server.close();
fs.writeFileSync(path.join(out, "lighthouse.json"), JSON.stringify(rows, null, 2));
