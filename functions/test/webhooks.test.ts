import Stripe from "stripe";
import { describe, expect, it } from "vitest";
import { createCheckoutSession } from "../src/checkout.js";
import { reconcileOrders } from "../src/fulfillment.js";
import { handlePrintifyWebhook } from "../src/printify-webhook.js";
import { PrintifyAmbiguousError, PrintifyRejectedError, verifyPrintifySignature } from "../src/printify.js";
import { handleStripeWebhook } from "../src/stripe-webhook.js";
import { fakePrintify, memoryStore, sign, testCatalog } from "./helpers.js";

const stripe = new Stripe("sk_test_unused");
const STRIPE_SECRET = "whsec_test";
const PFY_SECRET = "pfy_secret";

async function setup() {
  const store = memoryStore();
  const printify = fakePrintify();
  const created = await createCheckoutSession(
    {
      stripe: { checkout: { sessions: { create: async () => ({ id: "cs_test_1", url: "https://x" }) } } } as never,
      store,
      catalog: testCatalog,
      siteUrl: "https://example.test",
      automaticTax: false,
    },
    { items: [{ productId: "shirt", variantId: "ivory-m", quantity: 2 }] },
  );
  expect(created.status).toBe(200);
  const deps = { stripe, webhookSecret: STRIPE_SECRET, store, printify, catalog: testCatalog };
  return { store, printify, deps };
}

function stripeEvent(type: string, over: Record<string, unknown> = {}, id = `evt_${type}_1`) {
  const session = {
    id: "cs_test_1",
    object: "checkout.session",
    payment_status: "paid",
    currency: "usd",
    amount_subtotal: 6400,
    amount_total: 7000,
    total_details: { amount_shipping: 599, amount_tax: 0 },
    payment_intent: "pi_1",
    customer_details: { email: "a@example.test", phone: "+15555550100", name: "Ada Lovelace" },
    collected_information: {
      shipping_details: {
        name: "Ada Lovelace",
        address: { line1: "1 Main St", line2: null, city: "Austin", state: "TX", postal_code: "78701", country: "US" },
      },
    },
    ...over,
  };
  const payload = JSON.stringify({ id, object: "event", type, data: { object: session } });
  const header = stripe.webhooks.generateTestHeaderString({ payload, secret: STRIPE_SECRET });
  return { raw: Buffer.from(payload), header };
}

describe("stripe webhook", () => {
  it("rejects bad or missing signatures and does nothing", async () => {
    const { deps, printify } = await setup();
    const { raw } = stripeEvent("checkout.session.completed");
    expect((await handleStripeWebhook(deps, raw, "t=1,v1=bad")).status).toBe(400);
    expect((await handleStripeWebhook(deps, raw, undefined)).status).toBe(400);
    expect(printify.created).toHaveLength(0);
  });

  it("paid session creates exactly one held Printify order with the session ID as external_id", async () => {
    const { deps, printify, store } = await setup();
    const { raw, header } = stripeEvent("checkout.session.completed");
    expect((await handleStripeWebhook(deps, raw, header)).status).toBe(200);
    expect(printify.created).toHaveLength(1);
    expect(printify.sent).toHaveLength(0); // manual approval
    const order = store.orders.get("cs_test_1")!;
    expect(order).toMatchObject({ status: "on_hold", printifyOrderId: "pfy-order-1", email: "a@example.test", amountTotal: 7000 });
  });

  it("survives duplicate and concurrent delivery without double submission", async () => {
    const { deps, printify } = await setup();
    const { raw, header } = stripeEvent("checkout.session.completed");
    const results = await Promise.all([1, 2, 3].map(() => handleStripeWebhook(deps, raw, header)));
    expect(results.every((r) => r.status === 200)).toBe(true);
    const again = await handleStripeWebhook(deps, raw, header);
    expect(again.status).toBe(200);
    expect(printify.created).toHaveLength(1);
  });

  it("does not fulfil delayed payment until it succeeds", async () => {
    const { deps, printify, store } = await setup();
    const pending = stripeEvent("checkout.session.completed", { payment_status: "unpaid" });
    await handleStripeWebhook(deps, pending.raw, pending.header);
    expect(printify.created).toHaveLength(0);
    expect(store.orders.get("cs_test_1")!.status).toBe("awaiting_payment");

    const ok = stripeEvent("checkout.session.async_payment_succeeded");
    await handleStripeWebhook(deps, ok.raw, ok.header);
    expect(printify.created).toHaveLength(1);
  });

  it("marks payment failure and expiry without submitting", async () => {
    const { deps, printify, store } = await setup();
    const failed = stripeEvent("checkout.session.async_payment_failed", { payment_status: "unpaid" });
    await handleStripeWebhook(deps, failed.raw, failed.header);
    expect(store.orders.get("cs_test_1")!.status).toBe("payment_failed");
    expect(printify.created).toHaveLength(0);
  });

  it("marks unpaid expired sessions (cancellation) as expired", async () => {
    const { deps, store } = await setup();
    const e = stripeEvent("checkout.session.expired", { payment_status: "unpaid" });
    await handleStripeWebhook(deps, e.raw, e.header);
    expect(store.orders.get("cs_test_1")!.status).toBe("expired");
  });

  it("flags amount mismatches for review instead of submitting", async () => {
    const { deps, printify, store } = await setup();
    const e = stripeEvent("checkout.session.completed", { amount_subtotal: 100 });
    await handleStripeWebhook(deps, e.raw, e.header);
    expect(printify.created).toHaveLength(0);
    expect(store.orders.get("cs_test_1")!.status).toBe("needs_review");
  });

  it("returns 500 on a definite Printify rejection so Stripe retries, and the retry succeeds", async () => {
    const { deps, printify, store } = await setup();
    printify.failWith = new PrintifyRejectedError(422, "Printify rejected order create with HTTP 422");
    const { raw, header } = stripeEvent("checkout.session.completed");
    expect((await handleStripeWebhook(deps, raw, header)).status).toBe(500);
    expect(store.orders.get("cs_test_1")!.status).toBe("fulfillment_error");

    printify.failWith = undefined;
    expect((await handleStripeWebhook(deps, raw, header)).status).toBe(200);
    expect(printify.created).toHaveLength(1);
  });

  it("parks ambiguous Printify failures for human review and never auto-retries them", async () => {
    const { deps, printify, store } = await setup();
    printify.failWith = new PrintifyAmbiguousError("timeout");
    const { raw, header } = stripeEvent("checkout.session.completed");
    expect((await handleStripeWebhook(deps, raw, header)).status).toBe(200);
    expect(store.orders.get("cs_test_1")!.status).toBe("needs_review");

    printify.failWith = undefined;
    await handleStripeWebhook(deps, raw, header);
    expect(printify.created).toHaveLength(0);
  });

  it("rebuilds the order from metadata if the pre-create write was lost", async () => {
    const { deps, printify, store } = await setup();
    const token = store.orders.get("cs_test_1")!.publicToken;
    store.orders.clear();
    const e = stripeEvent("checkout.session.completed", { metadata: { publicToken: token, items: "shirt:ivory-m:2" } });
    await handleStripeWebhook(deps, e.raw, e.header);
    expect(printify.created).toHaveLength(1);
    expect(store.orders.get("cs_test_1")!.publicToken).toBe(token);
  });

  it("auto-approve sends to production; failure there never re-creates the order", async () => {
    const { deps, printify, store } = await setup();
    printify.sendToProduction = async () => {
      throw new PrintifyRejectedError(500, "boom");
    };
    const e = stripeEvent("checkout.session.completed");
    await handleStripeWebhook({ ...deps, fulfillment: { autoApprove: true } }, e.raw, e.header);
    expect(store.orders.get("cs_test_1")!.status).toBe("on_hold");
    await handleStripeWebhook({ ...deps, fulfillment: { autoApprove: true } }, e.raw, e.header);
    expect(printify.created).toHaveLength(1);
  });
});

describe("reconciliation", () => {
  it("retries stale paid orders and flags stuck submissions", async () => {
    const { store, printify } = await setup();
    const old = Date.now() - 60 * 60 * 1000;
    store.orders.set("cs_test_1", { ...store.orders.get("cs_test_1")!, status: "paid", updatedAt: old, email: "a@example.test", shippingAddress: { name: "A B", line1: "1 St", line2: null, city: "Austin", state: "TX", postalCode: "78701", country: "US" } });
    store.orders.set("cs_stuck", { ...store.orders.get("cs_test_1")!, id: "cs_stuck", publicToken: "x", status: "submitting", updatedAt: old });
    const result = await reconcileOrders(store, printify);
    expect(result).toEqual({ retried: ["cs_test_1"], flagged: ["cs_stuck"] });
    expect(printify.created).toHaveLength(1);
    expect(store.orders.get("cs_stuck")!.status).toBe("needs_review");
  });
});

describe("printify webhook", () => {
  async function submitted() {
    const ctx = await setup();
    const { raw, header } = stripeEvent("checkout.session.completed");
    await handleStripeWebhook(ctx.deps, raw, header);
    return { ...ctx, pdeps: { store: ctx.store, webhookSecret: PFY_SECRET } };
  }
  const evt = (type: string, data: unknown = {}, id = `pfy_${type}`) =>
    Buffer.from(JSON.stringify({ id, type, resource: { id: "pfy-order-1", data } }));

  it("verifies signatures", () => {
    const body = Buffer.from("{}");
    expect(verifyPrintifySignature(body, sign("{}", PFY_SECRET), PFY_SECRET)).toBe(true);
    expect(verifyPrintifySignature(body, sign("{}", "other"), PFY_SECRET)).toBe(false);
    expect(verifyPrintifySignature(body, undefined, PFY_SECRET)).toBe(false);
    expect(verifyPrintifySignature(body, "sha256=short", PFY_SECRET)).toBe(false);
  });

  it("rejects unsigned requests", async () => {
    const { pdeps, store } = await submitted();
    const body = evt("order:shipment:created");
    expect((await handlePrintifyWebhook(pdeps, body, "sha256=00")).status).toBe(401);
    expect(store.orders.get("cs_test_1")!.status).toBe("on_hold");
  });

  it("walks production -> shipped with tracking, ignores replays and out-of-order events", async () => {
    const { pdeps, store } = await submitted();
    const send = (body: Buffer) => handlePrintifyWebhook(pdeps, body, sign(body.toString(), PFY_SECRET));

    await send(evt("order:sent-to-production"));
    expect(store.orders.get("cs_test_1")!.status).toBe("in_production");

    const shipped = evt("order:shipment:created", { carrier: { code: "usps", tracking_number: "9400", tracking_url: "https://t.example/9400" } });
    await send(shipped);
    expect(store.orders.get("cs_test_1")).toMatchObject({ status: "shipped", trackingNumber: "9400", trackingCarrier: "usps" });

    expect((await send(shipped)).body).toMatchObject({ duplicate: true });
    await send(evt("order:sent-to-production", {}, "pfy_late"));
    expect(store.orders.get("cs_test_1")!.status).toBe("shipped");

    await send(evt("order:shipment:delivered"));
    expect(store.orders.get("cs_test_1")!.status).toBe("delivered");
  });

  it("acknowledges events for unknown orders", async () => {
    const { pdeps } = await submitted();
    const body = Buffer.from(JSON.stringify({ id: "e", type: "order:updated", resource: { id: "someone-else", data: {} } }));
    expect((await handlePrintifyWebhook(pdeps, body, sign(body.toString(), PFY_SECRET))).status).toBe(200);
  });
});
