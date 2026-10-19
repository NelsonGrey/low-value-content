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
