import { randomBytes } from "node:crypto";
import { getFirestore } from "firebase-admin/firestore";
import { getApps, initializeApp } from "firebase-admin/app";
import type { Order, OrderStatus, PublicOrder } from "./types.js";

/**
 * Persistence boundary for orders. Every state change that guards a side effect
 * (claiming Printify submission, recording a webhook event) must be atomic, so
 * implementations expose those as single operations rather than get/set pairs.
 */
export interface OrderStore {
  get(id: string): Promise<Order | null>;
  getByToken(token: string): Promise<Order | null>;
  /** Create the order if absent; returns the stored order either way. */
  createIfAbsent(order: Order): Promise<Order>;
  /** Atomically apply `patch` only when current status is in `from`. Returns the new order, or null if the guard failed. */
  transition(id: string, from: OrderStatus[], patch: Partial<Order>): Promise<Order | null>;
  /** Unconditional patch (used for webhook-driven status mirrors). */
  update(id: string, patch: Partial<Order>): Promise<Order | null>;
  /** Atomically record an event ID; returns false if it was already recorded. */
  recordEvent(id: string, eventId: string): Promise<boolean>;
  findByPrintifyOrderId(printifyOrderId: string): Promise<Order | null>;
  listByStatus(statuses: OrderStatus[], olderThanMs: number): Promise<Order[]>;
}

export function newPublicToken(): string {
  return randomBytes(24).toString("base64url");
}

export const PUBLIC_TOKEN_PATTERN = /^[A-Za-z0-9_-]{32}$/;

export function toPublicOrder(order: Order): PublicOrder {
  return {
    status: order.status,
    items: order.lines.map(({ productId, variantId, quantity }) => ({ productId, variantId, quantity })),
    currency: order.currency,
    amountTotal: order.amountTotal,
    trackingCarrier: order.trackingCarrier,
    trackingNumber: order.trackingNumber,
    trackingUrl: order.trackingUrl,
  };
}

const COLLECTION = "orders";

export function firestoreOrderStore(): OrderStore {
  if (getApps().length === 0) initializeApp();
  const db = getFirestore();
  const col = db.collection(COLLECTION);

  const first = async (q: FirebaseFirestore.Query): Promise<Order | null> => {
    const snap = await q.limit(1).get();
    return snap.empty ? null : (snap.docs[0]!.data() as Order);
  };

  return {
    async get(id) {
      const snap = await col.doc(id).get();
      return snap.exists ? (snap.data() as Order) : null;
    },
    getByToken: (token) => first(col.where("publicToken", "==", token)),
    findByPrintifyOrderId: (pid) => first(col.where("printifyOrderId", "==", pid)),
    async createIfAbsent(order) {
      return db.runTransaction(async (tx) => {
        const ref = col.doc(order.id);
        const snap = await tx.get(ref);
        if (snap.exists) return snap.data() as Order;
        tx.set(ref, order);
        return order;
      });
    },
    async transition(id, from, patch) {
      return db.runTransaction(async (tx) => {
        const ref = col.doc(id);
        const snap = await tx.get(ref);
        if (!snap.exists) return null;
        const current = snap.data() as Order;
        if (!from.includes(current.status)) return null;
        const next = { ...current, ...patch, updatedAt: Date.now() };
        tx.set(ref, next);
        return next;
      });
    },
    async update(id, patch) {
      return db.runTransaction(async (tx) => {
        const ref = col.doc(id);
        const snap = await tx.get(ref);
        if (!snap.exists) return null;
        const next = { ...(snap.data() as Order), ...patch, updatedAt: Date.now() };
        tx.set(ref, next);
        return next;
      });
    },
    async recordEvent(id, eventId) {
      return db.runTransaction(async (tx) => {
        const ref = col.doc(id);
        const snap = await tx.get(ref);
        if (!snap.exists) return false;
        const current = snap.data() as Order;
        if (current.processedEventIds.includes(eventId)) return false;
        tx.update(ref, {
          processedEventIds: [...current.processedEventIds, eventId].slice(-50),
          updatedAt: Date.now(),
        });
        return true;
      });
    },
    async listByStatus(statuses, olderThanMs) {
      const cutoff = Date.now() - olderThanMs;
      const snap = await col.where("status", "in", statuses).where("updatedAt", "<", cutoff).limit(100).get();
      return snap.docs.map((d) => d.data() as Order);
    },
  };
}
