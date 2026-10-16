import manifest from "../../../docs/product/apparel-manifest.json";

export type Product = (typeof manifest.launchProducts)[number];
export type LineageEntry = (typeof manifest.lineage)[number];

export const brand = manifest.brand;
export const products = manifest.launchProducts as Product[];
export const lineage = manifest.lineage as LineageEntry[];
export const observances = manifest.observances;
export const houses = manifest.houses;

export const originalProducts = products.filter((product) => product.position <= 6);
export const royalProducts = products.filter((product) => product.position > 6);

export const productImage = (product: Product): string | null => {
  const storefrontImage = "storefrontImage" in product.assets ? product.assets.storefrontImage : undefined;
  if (storefrontImage) return `/assets/${storefrontImage.split("/").pop()}`;
  return null;
};

export const productHref = (product: Product) => `/products/${product.id}.html`;
