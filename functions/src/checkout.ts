import type Stripe from "stripe";
import {
  CURRENCY,
  MAX_QUANTITY_PER_LINE,
  SHIPPING_AMOUNT,
  SHIPPING_COUNTRIES,
  isSellable,
  type Catalog,
} from "./catalog.js";
import { json, logFailure, type HttpResult } from "./http.js";
import { newPublicToken, type OrderStore } from "./orders.js";
import type { Order, OrderLine } from "./types.js";

export interface CheckoutDeps {
  stripe: Pick<Stripe, "checkout">;
  store: OrderStore;
  catalog: Catalog;
  siteUrl: string;
  automaticTax: boolean;
}

const MAX_LINES = 6;

type ParsedLines = { ok: true; lines: OrderLine[] } | { ok: false; error: string };

/** Turn untrusted {productId, variantId, quantity} requests into catalog-priced lines. */
export function resolveLines(catalog: Catalog, raw: unknown): ParsedLines {
  if (!Array.isArray(raw) || raw.length === 0 || raw.length > MAX_LINES) {
    return { ok: false, error: "items must be a non-empty list" };
  }
  const merged = new Map<string, OrderLine>();
  for (const item of raw as Record<string, unknown>[]) {
    if (typeof item !== "object" || item === null) return { ok: false, error: "invalid item" };
    const { productId, variantId, quantity } = item;
    if (typeof productId !== "string" || typeof variantId !== "string") return { ok: false, error: "invalid item" };
    if (!Number.isInteger(quantity) || (quantity as number) < 1 || (quantity as number) > MAX_QUANTITY_PER_LINE) {
      return { ok: false, error: "invalid quantity" };
    }
    const product = Object.hasOwn(catalog, productId) ? catalog[productId] : undefined;
    const variant = product && Object.hasOwn(product.variants, variantId) ? product.variants[variantId] : undefined;
    if (!product || !variant || !isSellable(product) || variant.printifyVariantId <= 0) {
      return { ok: false, error: "item unavailable" };
    }
    const key = `${productId}:${variantId}`;
    const existing = merged.get(key);
    const total = (existing?.quantity ?? 0) + (quantity as number);
    if (total > MAX_QUANTITY_PER_LINE) return { ok: false, error: "invalid quantity" };
    merged.set(key, {
      productId,
      variantId,
      quantity: total,
      unitAmount: product.unitAmount,
      printifyProductId: product.printifyProductId,
      printifyVariantId: variant.printifyVariantId,
    });
  }
  return { ok: true, lines: [...merged.values()] };
}

/** Compact form that fits Stripe's 500-character metadata value limit. */
export const encodeLines = (lines: OrderLine[]): string =>
  lines.map((l) => `${l.productId}:${l.variantId}:${l.quantity}`).join(",");

export function decodeLines(catalog: Catalog, encoded: string | undefined): OrderLine[] | null {
  if (!encoded) return null;
  const raw = encoded.split(",").map((part) => {
    const [productId, variantId, qty] = part.split(":");
    return { productId, variantId, quantity: Number(qty) };
  });
  const parsed = resolveLines(catalog, raw);
  return parsed.ok ? parsed.lines : null;
}

export async function createCheckoutSession(deps: CheckoutDeps, body: unknown): Promise<HttpResult> {
  const items = (body as { items?: unknown } | null)?.items;
  const parsed = resolveLines(deps.catalog, items);
  if (!parsed.ok) return json(400, { error: parsed.error });

  const publicToken = newPublicToken();
  try {
    const session = await deps.stripe.checkout.sessions.create({
      mode: "payment",
      line_items: parsed.lines.map((l) => {
        const product = deps.catalog[l.productId]!;
        return {
          quantity: l.quantity,
          price_data: {
            currency: CURRENCY,
            unit_amount: l.unitAmount,
            product_data: { name: `${product.name} · ${product.variants[l.variantId]!.label}` },
          },
        };
      }),
      shipping_address_collection: { allowed_countries: [...SHIPPING_COUNTRIES] },
      phone_number_collection: { enabled: true },
      shipping_options: [
        {
          shipping_rate_data: {
            display_name: "Standard shipping (US)",
            type: "fixed_amount",
            fixed_amount: { amount: SHIPPING_AMOUNT, currency: CURRENCY },
          },
        },
      ],
      automatic_tax: { enabled: deps.automaticTax },
      metadata: { publicToken, items: encodeLines(parsed.lines) },
      expires_at: Math.floor(Date.now() / 1000) + 31 * 60,
      success_url: `${deps.siteUrl}/order?token=${publicToken}`,
      cancel_url: `${deps.siteUrl}/shop`,
    });
    if (!session.url) throw new Error("Stripe returned no checkout URL");

    const now = Date.now();
    const order: Order = {
      id: session.id,
      publicToken,
      status: "awaiting_payment",
      lines: parsed.lines,
      currency: CURRENCY,
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
    };
    // If this write fails the webhook rebuilds the order from session metadata.
    await deps.store.createIfAbsent(order).catch((e) => logFailure("order_precreate_failed", { name: (e as Error).name }));
    return json(200, { url: session.url });
  } catch (err) {
    logFailure("checkout_session_failed", { name: (err as Error).name });
    return json(502, { error: "Could not start checkout" });
  }
}
