// Authoritative product data. The browser only ever sends product and variant
// identifiers; every price, Printify ID and quantity limit comes from here.

export interface CatalogVariant {
  label: string;
  /** Printify variant ID for this garment size/color on the chosen provider. */
  printifyVariantId: number;
}

export interface CatalogProduct {
  name: string;
  /** Unit price in the smallest currency unit (cents). */
  unitAmount: number;
  /** Printify product ID created in the Printify shop for this design. */
  printifyProductId: string;
  variants: Record<string, CatalogVariant>;
}

export type Catalog = Record<string, CatalogProduct>;

export const CURRENCY = "usd";
export const MAX_QUANTITY_PER_LINE = 5;

/** Fixed US shipping charged at checkout, in cents. */
export const SHIPPING_AMOUNT = 599;
export const SHIPPING_COUNTRIES = ["US"] as const;

// Printify IDs come from GET /v1/shops/{shop_id}/products/{product_id}.json (see tools/printify/).
// Only variants listed here can be bought. Add a sizes/colors line per enabled Printify variant.
// Prices are placeholders until the price test is decided.
export const PLACEHOLDER_PRINTIFY_PRODUCT_ID = "REPLACE_WITH_PRINTIFY_PRODUCT_ID";

export const catalog: Catalog = {
  validate: {
    name: "Please validate me algorithmically.",
    unitAmount: 3200,
    printifyProductId: "6af3d07784c3e9e3630dd1a6",
    variants: {
      "ivory-s": { label: "Ivory / S", printifyVariantId: 78991 },
      "ivory-m": { label: "Ivory / M", printifyVariantId: 78992 },
      "ivory-l": { label: "Ivory / L", printifyVariantId: 78993 },
      "ivory-xl": { label: "Ivory / XL", printifyVariantId: 78994 },
      "ivory-2xl": { label: "Ivory / 2XL", printifyVariantId: 78995 },
      "ivory-3xl": { label: "Ivory / 3XL", printifyVariantId: 79142 },
    },
  },
  "thought-leader": {
    name: "Thought leader. No thoughts required.",
    unitAmount: 3200,
    printifyProductId: "6af3d07bb0bec49fb208604b",
    variants: {
      "true-navy-s": { label: "True Navy / S", printifyVariantId: 79081 },
      "true-navy-m": { label: "True Navy / M", printifyVariantId: 79082 },
      "true-navy-l": { label: "True Navy / L", printifyVariantId: 79083 },
      "true-navy-xl": { label: "True Navy / XL", printifyVariantId: 79084 },
      "true-navy-2xl": { label: "True Navy / 2XL", printifyVariantId: 79085 },
      "true-navy-3xl": { label: "True Navy / 3XL", printifyVariantId: 79164 },
    },
  },
  doomscrolling: {
    name: "I'm not doomscrolling. I'm doing market research.",
    unitAmount: 3200,
    printifyProductId: "6af3d07ff6491c921e01d872",
    variants: {
      "brick-s": { label: "Brick / S", printifyVariantId: 78901 },
      "brick-m": { label: "Brick / M", printifyVariantId: 78902 },
      "brick-l": { label: "Brick / L", printifyVariantId: 78903 },
      "brick-xl": { label: "Brick / XL", printifyVariantId: 78904 },
      "brick-2xl": { label: "Brick / 2XL", printifyVariantId: 78905 },
      "brick-3xl": { label: "Brick / 3XL", printifyVariantId: 79119 },
    },
  },
  "content-creator": {
    name: "Content creator. Uniqueness questionable. Monetization inconsistent. Visibility unreported.",
    unitAmount: 3200,
    printifyProductId: "6af3d082c783a6d305012fce",
    variants: {
      "ivory-s": { label: "Ivory / S", printifyVariantId: 78991 },
      "ivory-m": { label: "Ivory / M", printifyVariantId: 78992 },
      "ivory-l": { label: "Ivory / L", printifyVariantId: 78993 },
      "ivory-xl": { label: "Ivory / XL", printifyVariantId: 78994 },
      "ivory-2xl": { label: "Ivory / 2XL", printifyVariantId: 78995 },
      "ivory-3xl": { label: "Ivory / 3XL", printifyVariantId: 79142 },
    },
  },
  "authentic-self": {
    name: "My authentic self is currently being monetized.",
    unitAmount: 3200,
    printifyProductId: "6af3d08684c3e9e3630dd1b1",
    variants: {
      "brick-s": { label: "Brick / S", printifyVariantId: 78901 },
      "brick-m": { label: "Brick / M", printifyVariantId: 78902 },
      "brick-l": { label: "Brick / L", printifyVariantId: 78903 },
      "brick-xl": { label: "Brick / XL", printifyVariantId: 78904 },
      "brick-2xl": { label: "Brick / 2XL", printifyVariantId: 78905 },
      "brick-3xl": { label: "Brick / 3XL", printifyVariantId: 79119 },
    },
  },
  "sent-regretted": {
    name: "Sent 2:14 AM. Regretted 2:15 AM.",
    unitAmount: 3200,
    printifyProductId: "6af3d08bf44a1129e5058223",
    variants: {
      "true-navy-s": { label: "True Navy / S", printifyVariantId: 79081 },
      "true-navy-m": { label: "True Navy / M", printifyVariantId: 79082 },
      "true-navy-l": { label: "True Navy / L", printifyVariantId: 79083 },
      "true-navy-xl": { label: "True Navy / XL", printifyVariantId: 79084 },
      "true-navy-2xl": { label: "True Navy / 2XL", printifyVariantId: 79085 },
      "true-navy-3xl": { label: "True Navy / 3XL", printifyVariantId: 79164 },
    },
  },
};

export function isSellable(product: CatalogProduct): boolean {
  return product.printifyProductId !== PLACEHOLDER_PRINTIFY_PRODUCT_ID;
}
