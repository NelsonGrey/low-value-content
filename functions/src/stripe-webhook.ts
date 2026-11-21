import type Stripe from "stripe";
import type { Catalog } from "./catalog.js";
import { decodeLines } from "./checkout.js";
import { fulfillOrder, type FulfillmentOptions } from "./fulfillment.js";
import { json, logFailure, type HttpResult } from "./http.js";
import { PUBLIC_TOKEN_PATTERN, type OrderStore } from "./orders.js";
import type { PrintifyClient } from "./printify.js";
import type { Order, ShippingAddress } from "./types.js";

export interface StripeWebhookDeps {
  stripe: Pick<Stripe, "webhooks">;
  webhookSecret: string;
  store: OrderStore;
  printify: PrintifyClient;
  catalog: Catalog;
  fulfillment?: FulfillmentOptions;
}

function shippingFrom(session: Stripe.Checkout.Session): ShippingAddress | null {
  // Stripe moved this field in API version 2025-03-31; accept both shapes.
  const details =
    session.collected_information?.shipping_details ??
    (session as unknown as { shipping_details?: Stripe.Checkout.Session.CollectedInformation.ShippingDetails })
      .shipping_details;
  const a = details?.address;
  if (!details || !a?.line1 || !a.city || !a.postal_code || !a.country) return null;
  return {
    name: details.name ?? session.customer_details?.name ?? "",
    line1: a.line1,
    line2: a.line2 ?? null,
    city: a.city,
    state: a.state ?? "",
    postalCode: a.postal_code,
    country: a.country,
  };
}

/** Ensure an order exists for the session, rebuilding from metadata if the pre-create write was lost. */
async function ensureOrder(deps: StripeWebhookDeps, session: Stripe.Checkout.Session): Promise<Order | null> {
  const existing = await deps.store.get(session.id);
  if (existing) return existing;
  const lines = decodeLines(deps.catalog, session.metadata?.items);
  const token = session.metadata?.publicToken;
  if (!lines || !token || !PUBLIC_TOKEN_PATTERN.test(token)) return null;
  const now = Date.now();
  return deps.store.createIfAbsent({
    id: session.id,
    publicToken: token,
    status: "awaiting_payment",
    lines,
    currency: session.currency ?? "usd",
    amountSubtotal: null,
    amountShipping: null,
    amountTax: null,
    amountTotal: null,
    stripePaymentIntentId: null,
    email: null,
    phone: null,
    shippingAddress: null,
    printifyOrderId: null,
    trackingCarrier: null,
    trackingNumber: null,
    trackingUrl: null,
    lastError: null,
    processedEventIds: [],
    createdAt: now,
    updatedAt: now,
  });
}

async function handlePaid(deps: StripeWebhookDeps, session: Stripe.Checkout.Session): Promise<"ok" | "retry"> {
  const order = await ensureOrder(deps, session);
  if (!order) {
    logFailure("stripe_session_unrecognized", { session: session.id });
    return "ok"; // nothing we can ever do with it; do not make Stripe retry for days
  }

  const expectedSubtotal = order.lines.reduce((sum, l) => sum + l.unitAmount * l.quantity, 0);
  const mismatch =
    session.currency !== order.currency || (session.amount_subtotal ?? expectedSubtotal) !== expectedSubtotal;
  const shippingAddress = shippingFrom(session);
  const missingInfo = !shippingAddress || !session.customer_details?.email;

  const paid = await deps.store.transition(order.id, ["awaiting_payment", "expired", "payment_failed"], {
    status: mismatch || missingInfo ? "needs_review" : "paid",
    lastError: mismatch
      ? "Paid amount does not match catalog snapshot"
      : missingInfo
        ? "Paid session lacks shipping address or email"
        : null,
    amountSubtotal: session.amount_subtotal,
    amountShipping: session.total_details?.amount_shipping ?? null,
    amountTax: session.total_details?.amount_tax ?? null,
    amountTotal: session.amount_total,
    stripePaymentIntentId: typeof session.payment_intent === "string" ? session.payment_intent : (session.payment_intent?.id ?? null),
    email: session.customer_details?.email ?? null,
    phone: session.customer_details?.phone ?? null,
    shippingAddress,
  });
  // A null transition means we already moved past awaiting_payment (duplicate delivery); fulfillment is still safe to attempt.

  if (paid?.status === "needs_review") return "ok";
  const result = await fulfillOrder(deps.store, deps.printify, order.id, deps.fulfillment);
  return result === "failed" ? "retry" : "ok";
}

export async function handleStripeWebhook(
  deps: StripeWebhookDeps,
  rawBody: Buffer,
  signature: string | undefined,
): Promise<HttpResult> {
  let event: Stripe.Event;
  try {
    if (!signature) throw new Error("missing signature");
    event = deps.stripe.webhooks.constructEvent(rawBody, signature, deps.webhookSecret);
  } catch {
    return json(400, { error: "Invalid signature" });
  }

  const session = event.data.object as Stripe.Checkout.Session;
  const isSessionEvent = event.type.startsWith("checkout.session.");
  if (!isSessionEvent) return json(200, { received: true });

  try {
    const known = await deps.store.get(session.id);
    if (known?.processedEventIds.includes(event.id)) return json(200, { received: true, duplicate: true });

    let outcome: "ok" | "retry" = "ok";
    switch (event.type) {
      case "checkout.session.completed":
        // Delayed payment methods complete as "unpaid"; wait for async_payment_succeeded.
        if (session.payment_status === "paid" || session.payment_status === "no_payment_required") {
          outcome = await handlePaid(deps, session);
        }
        break;
      case "checkout.session.async_payment_succeeded":
        outcome = await handlePaid(deps, session);
        break;
      case "checkout.session.async_payment_failed":
        await deps.store.transition(session.id, ["awaiting_payment"], { status: "payment_failed" });
        break;
      case "checkout.session.expired":
        await deps.store.transition(session.id, ["awaiting_payment"], { status: "expired" });
        break;
    }

    if (outcome === "retry") return json(500, { error: "Fulfillment failed; will retry" });
    await deps.store.recordEvent(session.id, event.id);
    return json(200, { received: true });
  } catch (err) {
    logFailure("stripe_webhook_failed", { type: event.type, session: session.id, name: (err as Error).name });
    return json(500, { error: "Processing failed" });
  }
}
