export type OrderStatus =
  | "awaiting_payment" // Checkout Session created, not yet paid
  | "paid" // payment confirmed, Printify order not yet created
  | "submitting" // Printify create call in flight (claimed)
  | "on_hold" // Printify order exists, awaiting manual production approval
  | "in_production"
  | "shipped"
  | "delivered"
  | "canceled" // Printify order canceled
  | "payment_failed"
  | "expired" // Checkout Session expired unpaid
  | "fulfillment_error" // definite Printify rejection; safe to retry
  | "needs_review"; // ambiguous outcome; a human must check Printify before retrying

export interface OrderLine {
  productId: string;
  variantId: string;
  quantity: number;
  /** Snapshot of catalog data at purchase time. */
  unitAmount: number;
  printifyProductId: string;
  printifyVariantId: number;
}

export interface ShippingAddress {
  name: string;
  line1: string;
  line2: string | null;
  city: string;
  state: string;
  postalCode: string;
  country: string;
}

export interface Order {
  /** Stripe Checkout Session ID; doubles as the document ID and Printify external_id. */
  id: string;
  publicToken: string;
  status: OrderStatus;
  lines: OrderLine[];
  currency: string;
  amountSubtotal: number | null;
  amountShipping: number | null;
  amountTax: number | null;
  amountTotal: number | null;
  stripePaymentIntentId: string | null;
  email: string | null;
  phone: string | null;
  shippingAddress: ShippingAddress | null;
  printifyOrderId: string | null;
  trackingCarrier: string | null;
  trackingNumber: string | null;
  trackingUrl: string | null;
  lastError: string | null;
  processedEventIds: string[];
  createdAt: number;
  updatedAt: number;
}

/** Fields safe to show to the customer holding the public token. */
export interface PublicOrder {
  status: OrderStatus;
  items: { productId: string; variantId: string; quantity: number }[];
  currency: string;
  amountTotal: number | null;
  trackingCarrier: string | null;
  trackingNumber: string | null;
  trackingUrl: string | null;
}
