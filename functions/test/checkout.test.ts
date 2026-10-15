import { describe, expect, it, vi } from "vitest";
import { createCheckoutSession, decodeLines, encodeLines, resolveLines } from "../src/checkout.js";
import { memoryStore, testCatalog } from "./helpers.js";

function deps() {
  const create = vi.fn(async () => ({ id: "cs_test_1", url: "https://checkout.stripe.com/c/pay/cs_test_1" }));
  const store = memoryStore();
  return {
    create,
    store,
    deps: {
      stripe: { checkout: { sessions: { create } } } as never,
      store,
      catalog: testCatalog,
      siteUrl: "https://example.test",
      automaticTax: false,
    },
  };
}

describe("resolveLines", () => {
  it.each([
    ["unknown product", [{ productId: "nope", variantId: "ivory-m", quantity: 1 }]],
    ["unknown variant", [{ productId: "shirt", variantId: "pink-xxl", quantity: 1 }]],
    ["prototype key", [{ productId: "__proto__", variantId: "x", quantity: 1 }]],
    ["placeholder Printify product", [{ productId: "unsellable", variantId: "ivory-m", quantity: 1 }]],
    ["zero quantity", [{ productId: "shirt", variantId: "ivory-m", quantity: 0 }]],
    ["fractional quantity", [{ productId: "shirt", variantId: "ivory-m", quantity: 1.5 }]],
    ["huge quantity", [{ productId: "shirt", variantId: "ivory-m", quantity: 99 }]],
    ["string quantity", [{ productId: "shirt", variantId: "ivory-m", quantity: "1" }]],
    ["empty list", []],
    ["not a list", "shirt"],
  ])("rejects %s", (_name, items) => {
    expect(resolveLines(testCatalog, items).ok).toBe(false);
  });

  it("merges duplicates and ignores browser-supplied prices", () => {
    const r = resolveLines(testCatalog, [
      { productId: "shirt", variantId: "ivory-m", quantity: 1, unitAmount: 1, price: 1 },
      { productId: "shirt", variantId: "ivory-m", quantity: 2 },
    ]);
    expect(r).toMatchObject({ ok: true, lines: [{ quantity: 3, unitAmount: 3200, printifyVariantId: 101 }] });
  });

  it("rejects merged quantity over the limit", () => {
    const r = resolveLines(testCatalog, [
      { productId: "shirt", variantId: "ivory-m", quantity: 3 },
      { productId: "shirt", variantId: "ivory-m", quantity: 3 },
    ]);
    expect(r.ok).toBe(false);
  });

  it("round-trips metadata encoding", () => {
    const r = resolveLines(testCatalog, [{ productId: "shirt", variantId: "ivory-l", quantity: 2 }]);
    if (!r.ok) throw new Error("unexpected");
    expect(decodeLines(testCatalog, encodeLines(r.lines))).toEqual(r.lines);
    expect(decodeLines(testCatalog, "garbage")).toBeNull();
  });
});

describe("createCheckoutSession", () => {
  it("creates a session priced from the catalog and pre-creates the order", async () => {
    const { deps: d, create, store } = deps();
    const res = await createCheckoutSession(d, { items: [{ productId: "shirt", variantId: "ivory-m", quantity: 2 }] });
    expect(res).toEqual({ status: 200, body: { url: "https://checkout.stripe.com/c/pay/cs_test_1" } });
    const params = (create.mock.calls[0] as unknown[])[0] as any;
    expect(params.line_items[0].price_data.unit_amount).toBe(3200);
    expect(params.line_items[0].quantity).toBe(2);
    expect(params.shipping_address_collection.allowed_countries).toEqual(["US"]);
    expect(params.success_url).toMatch(/^https:\/\/example\.test\/order\?token=[\w-]{32}$/);
    const order = store.orders.get("cs_test_1")!;
    expect(order.status).toBe("awaiting_payment");
    expect(params.metadata.publicToken).toBe(order.publicToken);
  });

  it("returns 400 and never calls Stripe for invalid items", async () => {
    const { deps: d, create } = deps();
    const res = await createCheckoutSession(d, { items: [{ productId: "shirt", variantId: "bogus", quantity: 1 }] });
    expect(res.status).toBe(400);
    expect(create).not.toHaveBeenCalled();
  });

  it("returns 502 without leaking Stripe errors", async () => {
    const { deps: d, create } = deps();
    create.mockRejectedValueOnce(new Error("sk_test_secret exploded"));
    const res = await createCheckoutSession(d, { items: [{ productId: "shirt", variantId: "ivory-m", quantity: 1 }] });
    expect(res).toEqual({ status: 502, body: { error: "Could not start checkout" } });
  });
});
