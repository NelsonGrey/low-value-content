// Keeps the six Great House names ("House of Influence") on one line everywhere, at any width.
// Runs after `astro build` (npm "postbuild"): in each built page, outside <script> and <style>,
// the spaces inside a Great House name become non-breaking spaces.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../dist");
const NAME = /House of (Prompt|Scroll|Influence|Signal|Spam|Buffer)/g;
const SKIP = /<(script|style)\b[\s\S]*?<\/\1>/gi;
let changed = 0;

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith(".html")) {
      const html = fs.readFileSync(full, "utf8");
      const kept = [];
      const masked = html.replace(SKIP, (m) => `\u0000${kept.push(m) - 1}\u0000`);
      const fixed = masked.replace(NAME, (_m, house) => `House&nbsp;of&nbsp;${house}`).replace(/\u0000(\d+)\u0000/g, (_m, i) => kept[Number(i)]);
      if (fixed !== html) { fs.writeFileSync(full, fixed); changed++; }
    }
  }
}
walk(dist);
console.log(`nowrap-houses: updated ${changed} page(s)`);
