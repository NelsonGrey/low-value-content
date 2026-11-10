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

// Printify IDs come from GET /v1/shops/{shop_id}/products/{product_id}.json.
// Only variants listed here can be bought. Add a sizes/colors line per enabled Printify variant.
export const PLACEHOLDER_PRINTIFY_PRODUCT_ID = "REPLACE_WITH_PRINTIFY_PRODUCT_ID";

export const catalog: Catalog = {
  validate: {
    name: "Please validate me algorithmically.",
    unitAmount: 3200,
    printifyProductId: "6ad1477a5dcca28e4500da6f",
    variants: {
      // TODO: enable S, M, XL, 2XL (and the Ivory color) in Printify, then add them here.
      "white-l": { label: "White / L", printifyVariantId: 73207 },
    },
  },
};

export function isSellable(product: CatalogProduct): boolean {
  return product.printifyProductId !== PLACEHOLDER_PRINTIFY_PRODUCT_ID;
}
