import { createHmac } from "node:crypto";
import type { Catalog } from "../src/catalog.js";
import type { OrderStore } from "../src/orders.js";
import type { PrintifyClient } from "../src/printify.js";
import type { Order, OrderStatus } from "../src/types.js";

export const testCatalog: Catalog = {
  shirt: {
    name: "Test Shirt",
    unitAmount: 3200,
    printifyProductId: "pfy-product-1",
    variants: { "ivory-m": { label: "Ivory / M", printifyVariantId: 101 }, "ivory-l": { label: "Ivory / L", printifyVariantId: 102 } },
  },
  unsellable: {
    name: "Placeholder",
    unitAmount: 100,
    printifyProductId: "REPLACE_WITH_PRINTIFY_PRODUCT_ID",
    variants: { "ivory-m": { label: "Ivory / M", printifyVariantId: 0 } },
  },
};

export function memoryStore(): OrderStore & { orders: Map<string, Order> } {
  const orders = new Map<string, Order>();
  const find = (pred: (o: Order) => boolean) => [...orders.values()].find(pred) ?? null;
  return {
    orders,
    get: async (id) => orders.get(id) ?? null,
    getByToken: async (t) => find((o) => o.publicToken === t),
    findByPrintifyOrderId: async (p) => find((o) => o.printifyOrderId === p),
    createIfAbsent: async (o) => orders.get(o.id) ?? (orders.set(o.id, o), o),
    async transition(id, from, patch) {
      const cur = orders.get(id);
      if (!cur || !from.includes(cur.status)) return null;
      const next = { ...cur, ...patch, updatedAt: Date.now() };
      orders.set(id, next);
      return next;
    },
    async update(id, patch) {
      const cur = orders.get(id);
      if (!cur) return null;
      const next = { ...cur, ...patch, updatedAt: Date.now() };
      orders.set(id, next);
      return next;
    },
    async recordEvent(id, eventId) {
      const cur = orders.get(id);
      if (!cur || cur.processedEventIds.includes(eventId)) return false;
      cur.processedEventIds.push(eventId);
      return true;
    },
    listByStatus: async (statuses: OrderStatus[], olderThanMs) =>
      [...orders.values()].filter((o) => statuses.includes(o.status) && o.updatedAt < Date.now() - olderThanMs),
  };
}

export function fakePrintify(): PrintifyClient & { created: Order[]; sent: string[]; failWith?: Error } {
  const state = {
    created: [] as Order[],
    sent: [] as string[],
    failWith: undefined as Error | undefined,
    async createOrder(order: Order) {
      if (state.failWith) throw state.failWith;
      state.created.push(order);
      return { id: `pfy-order-${state.created.length}` };
    },
    async sendToProduction(id: string) {
      state.sent.push(id);
    },
  };
  return state;
}

export const sign = (body: string, secret: string) => `sha256=${createHmac("sha256", secret).update(body).digest("hex")}`;
