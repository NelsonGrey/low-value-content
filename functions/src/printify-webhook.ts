import { json, logFailure, type HttpResult } from "./http.js";
import type { OrderStore } from "./orders.js";
import { verifyPrintifySignature } from "./printify.js";
import type { OrderStatus } from "./types.js";

export interface PrintifyWebhookDeps {
  store: OrderStore;
  webhookSecret: string;
}

interface PrintifyEvent {
  id?: string;
  type?: string;
  resource?: {
    id?: string;
    data?: {
      status?: string;
      carrier?: { code?: string; tracking_number?: string; tracking_url?: string };
    };
  };
}

// Webhooks can arrive out of order; never move an order backwards.
const RANK: Partial<Record<OrderStatus, number>> = { on_hold: 1, in_production: 2, shipped: 3, delivered: 4 };

export async function handlePrintifyWebhook(
  deps: PrintifyWebhookDeps,
  rawBody: Buffer,
  signature: string | undefined,
): Promise<HttpResult> {
  if (!verifyPrintifySignature(rawBody, signature, deps.webhookSecret)) {
    return json(401, { error: "Invalid signature" });
  }
  let event: PrintifyEvent;
  try {
    event = JSON.parse(rawBody.toString("utf8")) as PrintifyEvent;
  } catch {
    return json(400, { error: "Invalid JSON" });
  }
  const printifyOrderId = event.resource?.id;
  if (!event.type || !printifyOrderId) return json(200, { received: true });

  try {
    const order = await deps.store.findByPrintifyOrderId(printifyOrderId);
    if (!order) return json(200, { received: true }); // not ours, or not yet linked; Printify will not need a retry
    if (event.id && order.processedEventIds.includes(event.id)) return json(200, { received: true, duplicate: true });

    const carrier = event.resource?.data?.carrier;
    let next: OrderStatus | null = null;
    switch (event.type) {
      case "order:sent-to-production":
        next = "in_production";
        break;
      case "order:shipment:created":
        next = "shipped";
        break;
      case "order:shipment:delivered":
        next = "delivered";
        break;
      case "order:updated":
        if (event.resource?.data?.status === "canceled") next = "canceled";
        break;
    }

    if (next) {
      const canAdvance =
        next === "canceled"
          ? order.status === "on_hold"
          : (RANK[next] ?? 0) > (RANK[order.status] ?? 0);
      const patch =
        carrier && (next === "shipped" || next === "delivered")
          ? {
              trackingCarrier: carrier.code ?? order.trackingCarrier,
              trackingNumber: carrier.tracking_number ?? order.trackingNumber,
              trackingUrl: carrier.tracking_url ?? order.trackingUrl,
            }
          : {};
      if (canAdvance) await deps.store.update(order.id, { status: next, ...patch });
      else if (Object.keys(patch).length) await deps.store.update(order.id, patch);
    }
    if (event.id) await deps.store.recordEvent(order.id, event.id);
    return json(200, { received: true });
  } catch (err) {
    logFailure("printify_webhook_failed", { type: event.type, name: (err as Error).name });
    return json(500, { error: "Processing failed" });
  }
}
