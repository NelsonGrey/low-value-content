import manifest from "../../docs/product/apparel-manifest.json";

export type Product = (typeof manifest.launchProducts)[number];
export type LineageEntry = (typeof manifest.lineage)[number];

export const brand = manifest.brand;
export const products = manifest.launchProducts as Product[];
export const lineage = manifest.lineage as LineageEntry[];
export const observances = manifest.observances;
export const houses = manifest.houses;
export const constitution = manifest.constitution;
export const peerage = manifest.peerage;
export const orders = manifest.orders;

export const originalProducts = products.filter((product) => product.position <= 6);
export const royalProducts = products.filter((product) => product.position > 6);
export const publicNotices = products.filter((product) => product.launchCollection === "Public Notices");
export const courtAndOrders = products.filter((product) => product.launchCollection === "Court & Orders");
export const royalCommemorations = products.filter((product) => product.launchCollection === "Royal Commemorations");

export const hasRealmProvenance = (product: Product) => product.realmIntensity !== "none";

export const productImage = (product: Product): string | null => {
  const frontArt = "frontArtDisplay" in product.assets ? product.assets.frontArtDisplay : undefined;
  if (frontArt) return `/assets/${frontArt.split("/").pop()}`;
  return null;
};

export const productHref = (product: Product) => `/products/${product.id}.html`;

export interface VariantOption {
  /** Catalog variant key: `<color>-<size>`, for example `ivory-l`. */
  key: string;
  color: string;
  size: string;
  label: string;
}

const SIZE_ORDER = ["xs", "s", "m", "l", "xl", "2xl", "3xl", "4xl"];
const titleCase = (value: string) => value.split("-").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");

/** Purchasable variants for a product, read from the manifest and ordered by size. Empty when nothing is sellable. */
export const variantOptions = (product: Product): VariantOption[] =>
  (product.commerce.enabledVariants as string[])
    .map((key) => {
      const cut = key.lastIndexOf("-");
      const color = key.slice(0, cut);
      const size = key.slice(cut + 1);
      return { key, color, size, label: `${titleCase(color)} / ${size.toUpperCase()}` };
    })
    .sort((a, b) => SIZE_ORDER.indexOf(a.size) - SIZE_ORDER.indexOf(b.size));

export const isPurchasable = (product: Product): boolean =>
  product.commerceStatus === "test-sellable" && Boolean(product.commerce.catalogKey) && variantOptions(product).length > 0;
