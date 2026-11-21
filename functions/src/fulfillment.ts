import { PrintifyAmbiguousError, PrintifyRejectedError, type PrintifyClient } from "./printify.js";
import type { OrderStore } from "./orders.js";
import type { Order } from "./types.js";

export interface FulfillmentOptions {
  /** When true, the Printify order is sent to production immediately. Launch default is false (manual approval). */
  autoApprove?: boolean;
}

export type FulfillResult = "submitted" | "already_submitted" | "not_paid" | "failed" | "needs_review";

/**
 * Submit a paid order to Printify exactly once.
 *
 * The paid -> submitting transition is atomic, so concurrent webhook deliveries
 * or a reconciliation run cannot both reach createOrder. The Stripe Checkout
 * Session ID is the Printify external_id.
 */
export async function fulfillOrder(
  store: OrderStore,
  printify: PrintifyClient,
  orderId: string,
  options: FulfillmentOptions = {},
): Promise<FulfillResult> {
  const claimed = await store.transition(orderId, ["paid", "fulfillment_error"], {
    status: "submitting",
    lastError: null,
  });
  if (!claimed) {
    const current = await store.get(orderId);
    if (!current) return "not_paid";
    if (current.status === "needs_review") return "needs_review";
    return current.printifyOrderId ? "already_submitted" : "not_paid";
  }

  try {
    const { id } = await printify.createOrder(claimed);
    await store.update(orderId, { status: "on_hold", printifyOrderId: id, lastError: null });
    if (options.autoApprove) {
      // The order now exists, so a failure here must never send us back through createOrder.
      try {
        await printify.sendToProduction(id);
        await store.update(orderId, { status: "in_production" });
      } catch (err) {
        await store.update(orderId, { lastError: `Auto-approve failed: ${(err as Error).message}` });
      }
    }
    return "submitted";
  } catch (err) {
    if (err instanceof PrintifyRejectedError) {
      await store.update(orderId, { status: "fulfillment_error", lastError: err.message });
      return "failed";
    }
    const message = err instanceof PrintifyAmbiguousError ? err.message : `Unexpected error: ${(err as Error).name}`;
    await store.update(orderId, { status: "needs_review", lastError: message });
    return "needs_review";
  }
}

const STALE_MS = 15 * 60 * 1000;

/**
 * Operational safety net: retry paid orders that never reached Printify and flag
 * orders stuck mid-submission for a human, since Printify cannot be queried by
 * external_id to prove whether the order was created.
 */
export async function reconcileOrders(
  store: OrderStore,
  printify: PrintifyClient,
  options: FulfillmentOptions = {},
): Promise<{ retried: Order["id"][]; flagged: Order["id"][] }> {
  const retried: string[] = [];
  const flagged: string[] = [];

  for (const order of await store.listByStatus(["paid", "fulfillment_error"], STALE_MS)) {
    await fulfillOrder(store, printify, order.id, options);
    retried.push(order.id);
  }
  for (const order of await store.listByStatus(["submitting"], STALE_MS)) {
    const moved = await store.transition(order.id, ["submitting"], {
      status: "needs_review",
      lastError: "Stuck in submitting; check Printify for an order with this external_id before retrying",
    });
    if (moved) flagged.push(order.id);
  }
  return { retried, flagged };
}
