import Stripe from "stripe";

/**
 * The one place that builds Stripe clients, per the Nelson Grey Stripe standard
 * (docs/engineering/stripe-standard.md).
 *
 * The API version is pinned on purpose and must equal the `api_version` of the
 * account's webhook endpoints: webhook payloads follow the endpoint's version,
 * not this client's. Bump both together with the `stripe` package, never
 * implicitly.
 */
export const STRIPE_API_VERSION = "2026-10-28.endive" as const;

/** Value written to `metadata.app` on every Stripe object this service creates. */
export const STRIPE_APP_NAME = "low-value-content";

/** `dev`, `staging` or `prod`, derived from the Firebase project id. */
export function stripeEnvName(): string {
  const project = (process.env.GCLOUD_PROJECT || process.env.GCP_PROJECT || "").toString();
  if (project.endsWith("-prod")) return "prod";
  if (project.endsWith("-staging")) return "staging";
  return "dev";
}

/** Standard metadata so one Stripe account can serve several products and environments. */
export function stripeMetadata(extra: Record<string, string> = {}): Record<string, string> {
  return { ...extra, app: STRIPE_APP_NAME, env: stripeEnvName() };
}

export function getStripe(secretKey: string): Stripe {
  return new Stripe(secretKey, {
    apiVersion: STRIPE_API_VERSION,
    maxNetworkRetries: 2,
    appInfo: { name: `${STRIPE_APP_NAME}-functions` },
  });
}
