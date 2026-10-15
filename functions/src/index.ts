import { onRequest } from "firebase-functions/v2/https";
import { onSchedule } from "firebase-functions/v2/scheduler";
import { defineSecret, defineString, defineBoolean } from "firebase-functions/params";
import Stripe from "stripe";
import { catalog } from "./catalog.js";
import { createCheckoutSession } from "./checkout.js";
import { reconcileOrders } from "./fulfillment.js";
import { json, type HttpResult } from "./http.js";
import { PUBLIC_TOKEN_PATTERN, firestoreOrderStore, toPublicOrder } from "./orders.js";
import { handlePrintifyWebhook } from "./printify-webhook.js";
import { printifyClient } from "./printify.js";
import { handleStripeWebhook } from "./stripe-webhook.js";

const stripeSecretKey = defineSecret("STRIPE_SECRET_KEY");
const stripeWebhookSecret = defineSecret("STRIPE_WEBHOOK_SECRET");
const printifyToken = defineSecret("PRINTIFY_API_TOKEN");
const printifyWebhookSecret = defineSecret("PRINTIFY_WEBHOOK_SECRET");
const printifyShopId = defineString("PRINTIFY_SHOP_ID");
const siteUrl = defineString("SITE_URL", { default: "https://lowvaluecontent.com" });
const automaticTax = defineBoolean("STRIPE_AUTOMATIC_TAX", { default: false });
// Launch default: orders stay on hold in Printify until approved manually.
const autoApprove = defineBoolean("PRINTIFY_AUTO_APPROVE", { default: false });

const secrets = [stripeSecretKey, stripeWebhookSecret, printifyToken, printifyWebhookSecret];

const stripe = () => new Stripe(stripeSecretKey.value());
const printify = () => printifyClient({ token: printifyToken.value(), shopId: printifyShopId.value() });

function send(res: import("firebase-functions/v2/https").Response, result: HttpResult): void {
  res.status(result.status).set("Cache-Control", "no-store").json(result.body);
}

export const api = onRequest({ secrets, region: "us-central1", maxInstances: 10 }, async (req, res) => {
  const store = firestoreOrderStore();
  const path = req.path.replace(/\/+$/, "");

  if (req.method === "POST" && path === "/api/checkout-session") {
    if (!req.is("application/json")) return send(res, json(415, { error: "Expected JSON" }));
    return send(
      res,
      await createCheckoutSession(
        { stripe: stripe(), store, catalog, siteUrl: siteUrl.value(), automaticTax: automaticTax.value() },
        req.body,
      ),
    );
  }

  if (req.method === "POST" && path === "/api/webhooks/stripe") {
    return send(
      res,
      await handleStripeWebhook(
        {
          stripe: stripe(),
          webhookSecret: stripeWebhookSecret.value(),
          store,
          printify: printify(),
          catalog,
          fulfillment: { autoApprove: autoApprove.value() },
        },
        req.rawBody,
        req.header("stripe-signature"),
      ),
    );
  }

  if (req.method === "POST" && path === "/api/webhooks/printify") {
    return send(
      res,
      await handlePrintifyWebhook(
        { store, webhookSecret: printifyWebhookSecret.value() },
        req.rawBody,
        req.header("x-pfy-signature"),
      ),
    );
  }

  const match = req.method === "GET" ? /^\/api\/orders\/([^/]+)$/.exec(path) : null;
  if (match) {
    const token = match[1]!;
    if (!PUBLIC_TOKEN_PATTERN.test(token)) return send(res, json(404, { error: "Not found" }));
    const order = await store.getByToken(token);
    return send(res, order ? json(200, toPublicOrder(order)) : json(404, { error: "Not found" }));
  }

  send(res, json(404, { error: "Not found" }));
});

export const reconcile = onSchedule(
  { schedule: "every 30 minutes", secrets: [printifyToken], region: "us-central1" },
  async () => {
    const result = await reconcileOrders(firestoreOrderStore(), printify(), { autoApprove: autoApprove.value() });
    console.log(JSON.stringify({ event: "reconcile", retried: result.retried.length, flagged: result.flagged.length }));
  },
);
