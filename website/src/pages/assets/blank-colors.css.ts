import { products } from "../../data";

// One CSS class per garment colour we sell, generated from the manifest so the colour
// customers see on the page can never differ from the blankColor we put on the order.
export function GET() {
  const colours = new Map<string, string>();
  for (const product of products) colours.set(product.blankColor.toLowerCase().replace(/ /g, "-"), product.garmentHex);
  const css = [...colours].map(([slug, hex]) => `.blank-${slug} { background: ${hex} !important; }`).join("\n") + "\n";
  return new Response(css, { headers: { "Content-Type": "text/css; charset=utf-8" } });
}
