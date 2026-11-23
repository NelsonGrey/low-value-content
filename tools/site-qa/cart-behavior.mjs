// One-off behavior test for the redesigned cart: quantities, totals, remove, empty state, checkout request.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright-core";

const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../website/dist");
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".woff2": "font/woff2" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  let file = path.join(dist, p);
  if (!fs.existsSync(file) && fs.existsSync(file + ".html")) file += ".html";
  if (!file.startsWith(dist) || !fs.existsSync(file)) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(0, r));
const base = `http://localhost:${server.address().port}`;
const browser = await chromium.launch({ channel: "chrome" });
const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();

let failures = 0;
const check = (name, ok, got) => { console.log(`${ok ? "PASS" : "FAIL"}  ${name}${ok ? "" : "  got: " + got}`); if (!ok) failures++; };
const text = (sel) => page.locator(sel).first().innerText();

// 1. Add from the product page through the real form, then open the cart.
await page.goto(`${base}/products/validate.html`, { waitUntil: "networkidle" });
await page.selectOption("select[name=size]", "m");
await page.click("button[type=submit]");
await page.goto(`${base}/cart.html`, { waitUntil: "networkidle" });
check("one line after add", (await page.locator(".cart-line").count()) === 1, await page.locator(".cart-line").count());
check("empty state hidden when filled", !(await page.locator("[data-cart-empty]").isVisible()), "visible");
check("subtotal $36.00", (await text("[data-cart-subtotal]")) === "$36.00", await text("[data-cart-subtotal]"));
check("shipping $5.99", (await text("[data-cart-shipping]")) === "$5.99", await text("[data-cart-shipping]"));
check("total $41.99", (await text("[data-cart-total]")) === "$41.99", await text("[data-cart-total]"));
check("label says 1 item", (await text("[data-cart-count-label]")) === "Subtotal (1 item)", await text("[data-cart-count-label]"));

// 2. Quantity change updates line total and summary.
await page.selectOption(".cart-line select", "3");
check("line total $108.00", (await text(".cart-line-total")) === "$108.00", await text(".cart-line-total"));
check("total $113.99", (await text("[data-cart-total]")) === "$113.99", await text("[data-cart-total]"));
check("label says 3 items", (await text("[data-cart-count-label]")) === "Subtotal (3 items)", await text("[data-cart-count-label]"));
check("header badge shows 3", (await text("[data-cart-count]")) === "3", await text("[data-cart-count]"));

// 3. Checkout posts the right payload (stubbed so no network or Stripe is touched).
let payload = null;
await page.route("**/api/checkout-session", async (route) => {
  payload = JSON.parse(route.request().postData());
  await route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ error: "stub" }) });
});
await page.click("[data-cart-checkout]");
await page.waitForFunction(() => /unavailable/i.test(document.querySelector(".cart-summary .buy-note").textContent));
check("checkout payload", JSON.stringify(payload) === JSON.stringify({ items: [{ productId: "validate", variantId: "ivory-m", quantity: 3 }] }), JSON.stringify(payload));
check("error shown and button re-enabled", await page.locator("[data-cart-checkout]").isEnabled(), "disabled");

// 4. Remove returns to the empty state with the six suggestions.
await page.click(".cart-line .link-button");
check("empty state shown", await page.locator("[data-cart-empty]").isVisible(), "hidden");
check("summary hidden", !(await page.locator("[data-cart-filled]").isVisible()), "visible");
check("six suggestions", (await page.locator(".cart-suggest li").count()) === 6, await page.locator(".cart-suggest li").count());
check("badge cleared", !(await page.locator("[data-cart-count]").first().isVisible()), "visible");

await browser.close();
server.close();
console.log(failures ? `${failures} FAILED` : "all passed");
process.exit(failures ? 1 : 0);
