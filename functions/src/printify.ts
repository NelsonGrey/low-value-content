import { createHmac, timingSafeEqual } from "node:crypto";
import type { Order } from "./types.js";

const API_BASE = "https://api.printify.com/v1";

/** The create call was rejected with an HTTP response: nothing was created, so a retry is safe. */
export class PrintifyRejectedError extends Error {
  constructor(readonly status: number, message: string) {
    super(message);
  }
}

/** No definite answer (timeout, network drop): an order may or may not exist. */
export class PrintifyAmbiguousError extends Error {}

export interface PrintifyClient {
  /** Creates an order that stays unsent: Printify only starts production after send_to_production. */
  createOrder(order: Order): Promise<{ id: string }>;
  sendToProduction(printifyOrderId: string): Promise<void>;
}

export interface PrintifyConfig {
  token: string;
  shopId: string;
  fetchImpl?: typeof fetch;
  timeoutMs?: number;
}

function splitName(full: string): { first_name: string; last_name: string } {
  const parts = full.trim().split(/\s+/);
  const first = parts.shift() ?? "";
  return { first_name: first, last_name: parts.join(" ") || first };
}

export function buildOrderPayload(order: Order) {
  if (!order.shippingAddress || !order.email) {
    throw new Error("Order is missing shipping address or email");
  }
  const a = order.shippingAddress;
  return {
    external_id: order.id,
    label: order.id.slice(-12),
    line_items: order.lines.map((l) => ({
      product_id: l.printifyProductId,
      variant_id: l.printifyVariantId,
      quantity: l.quantity,
    })),
    shipping_method: 1, // standard
    is_printify_express: false,
    send_shipping_notification: true,
    address_to: {
      ...splitName(a.name),
      email: order.email,
      phone: order.phone ?? "",
      country: a.country,
      region: a.state,
      address1: a.line1,
      address2: a.line2 ?? "",
      city: a.city,
      zip: a.postalCode,
    },
  };
}

export function printifyClient(config: PrintifyConfig): PrintifyClient {
  const doFetch = config.fetchImpl ?? fetch;
  const timeoutMs = config.timeoutMs ?? 20_000;
  const shop = encodeURIComponent(config.shopId);

  async function call(method: string, path: string, body?: unknown): Promise<Response> {
    try {
      return await doFetch(`${API_BASE}${path}`, {
        method,
        headers: {
          Authorization: `Bearer ${config.token}`,
          "Content-Type": "application/json;charset=utf-8",
          "User-Agent": "low-value-content-functions",
        },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: AbortSignal.timeout(timeoutMs),
      });
    } catch (err) {
      throw new PrintifyAmbiguousError(`Printify request failed without a response: ${(err as Error).name}`);
    }
  }

  return {
    async createOrder(order) {
      const res = await call("POST", `/shops/${shop}/orders.json`, buildOrderPayload(order));
      if (!res.ok) {
        // Body may echo customer data; keep only the status in logs and error state.
        throw new PrintifyRejectedError(res.status, `Printify rejected order create with HTTP ${res.status}`);
      }
      const json = (await res.json().catch(() => null)) as { id?: string } | null;
      if (!json?.id) throw new PrintifyAmbiguousError("Printify accepted the order but returned no ID");
      return { id: json.id };
    },
    async sendToProduction(printifyOrderId) {
      const res = await call("POST", `/shops/${shop}/orders/${encodeURIComponent(printifyOrderId)}/send_to_production.json`);
      if (!res.ok) throw new PrintifyRejectedError(res.status, `Printify send_to_production failed with HTTP ${res.status}`);
    },
  };
}

/** Printify signs the raw body with HMAC-SHA256 and sends it as `X-Pfy-Signature: sha256=<hex>`. */
export function verifyPrintifySignature(rawBody: Buffer, header: string | undefined, secret: string): boolean {
  if (!header) return false;
  const provided = header.startsWith("sha256=") ? header.slice(7) : header;
  const expected = createHmac("sha256", secret).update(rawBody).digest("hex");
  const a = Buffer.from(provided, "utf8");
  const b = Buffer.from(expected, "utf8");
  return a.length === b.length && timingSafeEqual(a, b);
}
