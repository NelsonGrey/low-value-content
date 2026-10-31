import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const conceptsPath = path.join(root, "docs/product/concept-catalog.md");
const manifestPath = path.join(root, "docs/product/apparel-manifest.json");
const jsonPath = path.join(root, "docs/product/ecosystem-apparel-catalog.json");
const markdownPath = path.join(root, "docs/product/ECOSYSTEM_APPAREL_CATALOG.md");

const collectionConfig = {
  "Social Media Theater": { house: "House of Influence", institution: "Chancery of Public Importance", form: "PN", garment: "Warm white or washed black", locus: "Realm / Influence" },
  "Algorithm Anxiety": { house: "House of Signal", institution: "Ministry of Measurable Outcomes", form: "PN", garment: "Warm white", locus: "Realm / Signal" },
  "Creator Economy": { house: "House of Influence", institution: "Chancery of Public Importance", form: "PN", garment: "Warm white or washed black", locus: "Realm / Influence" },
  "Chronically Online": { house: "House of Scroll", institution: "Royal Institute of Digital Inquiry", form: "PN", garment: "Oxblood or deep navy", locus: "Realm / Scroll" },
  "Artificial Authenticity": { house: "House of Prompt", institution: "Office of Synthetic Understanding", form: "PN", garment: "Warm ivory or deep navy", locus: "Realm / Prompt" },
  "Future of Work": { house: "House of Prompt", institution: "Office of Synthetic Understanding", form: "PN", garment: "Washed black or industrial ivory", locus: "Realm / Prompt" },
  "Productivity Theater": { house: "House of Signal", institution: "Ministry of Measurable Outcomes", form: "PN", garment: "Warm white or washed black", locus: "Realm / Signal" },
  "Performative Sustainability": { house: "House of Signal", institution: "Ministry of Measurable Outcomes", form: "PN", garment: "Warm ivory or faded green", locus: "Realm / Signal" },
  "Terms and Conditions": { house: "House of Spam", institution: "Ministry of Universal Correspondence", form: "PN", garment: "Warm white or washed black", locus: "Realm / Spam" },
  "Optimized Human": { house: "House of Signal", institution: "Ministry of Measurable Outcomes", form: "PN", garment: "Warm ivory or washed navy", locus: "Realm / Signal" },
};

const formOverrides = new Map([
  [1, "CO"], [9, "CO"], [15, "HW"], [24, "HW"], [31, "CO"], [33, "HW"],
  [42, "HW"], [46, "HW"], [50, "HW"], [51, "HW"], [52, "CO"], [56, "HW"],
  [57, "CO"], [68, "CO"], [75, "CO"], [76, "CO"], [88, "CO"],
  [60, "HW"], [74, "HW"], [91, "CO"], [99, "HW"],
]);

const houseOverrides = new Map([
  [11, "None required"], [12, "None required"], [13, "House of Buffer"],
  [15, "House of Buffer"], [17, "House of Prompt"], [20, "House of Buffer"],
  [21, "None required"], [22, "None required"], [24, "House of Scroll"],
  [31, "House of Scroll"], [32, "House of Buffer"], [33, "House of Scroll"],
  [37, "House of Buffer"], [38, "House of Influence"], [40, "House of Influence"],
  [42, "House of Prompt"], [44, "House of Prompt"], [46, "House of Buffer"],
  [49, "House of Buffer"], [50, "House of Signal"], [51, "House of Buffer"],
  [55, "House of Buffer"], [60, "House of Spam"], [68, "House of Buffer"],
  [70, "House of Buffer"], [74, "House of Spam"], [82, "House of Buffer"],
  [84, "House of Spam"], [89, "House of Signal"], [90, "House of Buffer"],
  [95, "House of Buffer"], [99, "House of Signal"],
]);

const formNames = {
  PN: "Public Notice",
  HW: "House Warrant",
  CO: "Court & Order",
  RC: "Royal Commemoration",
};

const printRules = {
  PN: "Front-only; typography or one familiar interface object; 1–2 inks; no sovereign heraldry; three short lines maximum.",
  HW: "Front-only; one large recognizable object plus one subordinate House badge; 2–4 inks; no sovereign supporters.",
  CO: "Front-only; centered seal, medal, certificate, or appointment device; 2–5 inks; English remains primary and Latin is subordinate.",
  RC: "Front-only; dated relic, specimen, or historical device; limited-color or approved full-color art; English title plus optional short Latin line.",
};

const normalize = (value) => value.toLowerCase().replace(/[’']/g, "'").replace(/[^a-z0-9]+/g, " ").trim();
const slugify = (value) => normalize(value).replace(/ /g, "-");

function buildArtworkPrompt({ form, saying, visual, house }) {
  const style = {
    PN: "Contemporary editorial print design with restrained typography and one familiar interface object at most; one or two flat inks; no heraldry.",
    HW: "Formal institutional warrant design with one large recognizable object and a small subordinate House device; two to four flat inks; no sovereign supporters or crown.",
    CO: "Ceremonial seal, medal, certificate, or appointment design with controlled antique ornament; English declaration dominant; two to five printable colors.",
    RC: "Rich archival commemorative illustration built around one historical relic or specimen; restrained antique ornament; English title dominant and Latin subordinate.",
  }[form];
  const houseInstruction = form === "PN" || house === "None required"
    ? "Do not add a House badge, crown, supporters, seal, Latin, or other Realm decoration."
    : `Use the canonical ${house} device only as a subordinate reference element; do not invent or redesign its arms.`;
  return `Use case: logo-brand. Asset type: isolated front-only apparel artwork. Primary request: ${visual}. Style: ${style} Text (verbatim): "${saying}" Constraints: one centered composition on a transparent background; exact text and no other primary wording; legible at 200 px; crisp separable edges; no garment, mannequin, room, props, shadows, watermark, or platform logo. ${houseInstruction}`;
}

function parseConcepts(markdown) {
  const concepts = [];
  let collection = "";
  for (const line of markdown.split("\n")) {
    const heading = line.match(/^## Collection \d+: (.+)$/);
    if (heading) collection = heading[1];
    const row = line.match(/^\| (\d+) \| (.*?) \| (.*?) \| (Launch|Develop|Hold) \|$/);
    if (!row) continue;
    concepts.push({
      sourceNumber: Number(row[1]),
      saying: row[2],
      originalVisualDirection: row[3],
      originalStatus: row[4],
      subjectCollection: collection,
    });
  }
  return concepts;
}

const concepts = parseConcepts(fs.readFileSync(conceptsPath, "utf8"));
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const foundingByCopy = new Map(manifest.launchProducts.map((product) => [normalize(product.primaryCopy), product]));
const promotedSourceNumbers = new Set();

const library = concepts.map((concept) => {
  const config = collectionConfig[concept.subjectCollection];
  const founding = foundingByCopy.get(normalize(concept.saying));
  if (founding) promotedSourceNumbers.add(concept.sourceNumber);
  const form = founding
    ? founding.launchCollection === "Public Notices" ? "PN" : founding.launchCollection === "Royal Commemorations" ? "RC" : "CO"
    : formOverrides.get(concept.sourceNumber) ?? config.form;
  const house = founding
    ? form === "PN" ? "None required" : founding.house ?? config.house
    : houseOverrides.get(concept.sourceNumber) ?? config.house;
  return {
    catalogId: `L${String(concept.sourceNumber).padStart(3, "0")}`,
    sourceNumber: concept.sourceNumber,
    saying: concept.saying,
    subjectCollection: concept.subjectCollection,
    catalogRole: founding ? `Promoted to Founding ${String(founding.position).padStart(2, "0")}` : "Expansion library",
    originalStatus: concept.originalStatus,
    issueForm: form,
    issueFormName: formNames[form],
    primaryHouse: house,
    institution: house === "None required" ? "None required" : config.institution,
    websiteLocus: founding ? `Regalia / ${founding.launchCollection}` : `${config.locus}; future catalog / ${slugify(concept.subjectCollection)}`,
    garmentDirection: founding ? null : config.garment,
    printRule: printRules[form],
    imageBrief: concept.originalVisualDirection,
    artworkPrompt: buildArtworkPrompt({ form, saying: concept.saying, visual: concept.originalVisualDirection, house }),
    exactText: concept.saying,
    creativeStage: founding ? founding.creativeStatus : concept.originalStatus === "Launch" ? "Expansion candidate" : concept.originalStatus === "Develop" ? "Development" : "Reserve",
    rightsStage: "Creative concept only; collision and legal clearance remain open",
    productionStage: founding ? "See Founding Ten record" : "No production artwork",
    foundingPosition: founding?.position ?? null,
  };
});

const founding = manifest.launchProducts.map((product) => {
  const form = product.launchCollection === "Public Notices" ? "PN" : product.launchCollection === "Royal Commemorations" ? "RC" : "CO";
  const foundingHouse = form === "PN" ? "None required" : product.house ?? "None required";
  return {
    catalogId: `F${String(product.position).padStart(2, "0")}`,
    productId: product.id,
    saying: product.primaryCopy,
    launchCollection: product.launchCollection,
    catalogRole: "Founding Ten",
    issueForm: form,
    issueFormName: formNames[form],
    primaryHouse: foundingHouse,
    institution: foundingHouse === "None required" ? "None required" : product.realmIssue?.office ?? "None required",
    websiteLocus: `Regalia / ${product.launchCollection}; product / ${product.id}`,
    garmentDirection: product.assets?.garmentColor ?? null,
    printRule: printRules[form],
    imageBrief: product.regaliaRole,
    artworkPrompt: buildArtworkPrompt({ form, saying: product.primaryCopy, visual: product.regaliaRole, house: foundingHouse }),
    exactText: product.primaryCopy,
    creativeStage: product.creativeStatus,
    rightsStage: "Creative concept only; collision and legal clearance remain open",
    productionStage: product.assets?.artwork
      ? `${product.creativeStatus === "ornate-art-plate" ? "Artwork plate (not print-ready)" : "Editable artwork"}: ${product.assets.artwork}`
      : "No production artwork",
    conceptMockup: product.assets?.conceptMockup ?? null,
    artworkPlate: [7, 8, 9, 10].includes(product.position)
      ? `design/mockups/royal-house/A${String(product.position).padStart(2, "0")}-${product.position === 7 ? "much-published-little-said" : product.position === 8 ? "order-blue-check" : product.position === 9 ? "y2k-postponed" : "patron-saint-debugging"}.png`
      : null,
  };
});

const priorityIds = ["L002", "L023", "L061", "L081", "L015", "L024", "L042", "L051", "L052", "L068", "L076", "L088"];
const priorityExpansionTranche = priorityIds.map((id) => library.find((item) => item.catalogId === id));

const catalog = {
  schemaVersion: 1,
  generatedOn: "2026-10-19",
  status: "working commercial-creative catalog; not rights-cleared or print-approved",
  counts: {
    foundingProducts: founding.length,
    originalConcepts: library.length,
    originalConceptsPromotedToFounding: promotedSourceNumbers.size,
    unpromotedExpansionConcepts: library.length - promotedSourceNumbers.size,
    uniqueProducts: founding.length + library.length - promotedSourceNumbers.size,
  },
  issueForms: Object.entries(formNames).map(([code, name]) => ({ code, name, printRule: printRules[code] })),
  founding,
  priorityExpansionTranche,
  library,
};

const collectionRows = Object.entries(collectionConfig).map(([name, config]) => {
  const entries = library.filter((item) => item.subjectCollection === name);
  return `| ${name} | ${config.house} | ${config.institution} | ${config.form} | ${config.garment} | ${entries.filter((item) => !item.foundingPosition).length} |`;
}).join("\n");

const foundingRows = founding.map((item) => `| ${item.catalogId} | ${item.saying} | ${item.launchCollection} | ${item.issueForm} | ${item.primaryHouse} | ${item.productionStage} |`).join("\n");
const priorityRows = priorityExpansionTranche.map((item) => `| ${item.catalogId} | ${item.saying} | ${item.subjectCollection} | ${item.issueForm} | ${item.primaryHouse} | ${item.imageBrief} |`).join("\n");

const librarySections = Object.keys(collectionConfig).map((collectionName) => {
  const rows = library.filter((item) => item.subjectCollection === collectionName).map((item) =>
    `| ${item.catalogId} | ${item.saying} | ${item.issueForm} | ${item.primaryHouse} | ${item.imageBrief} | ${item.catalogRole} | ${item.creativeStage} |`
  ).join("\n");
  return `## ${collectionName}\n\n| ID | Exact front declaration | Form | House | Printable visual brief | Catalog role | Stage |\n|---|---|---|---|---|---|---|\n${rows}`;
}).join("\n\n");

const markdown = `# Ecosystem Apparel Catalog\n\nStatus: working commercial-creative source of truth. Nothing in this document is trademark-cleared, marketplace-cleared, provider-approved, sampled, or authorized for sale unless a later production record says so.\n\n## What this catalog resolves\n\nThe project contains 100 original concepts. Six were promoted into the Founding Ten, and four Realm-native products were added. The complete ecosystem therefore contains **104 unique product concepts**: ten Founding products plus ninety-four unpromoted expansion concepts.\n\nThis catalog connects every concept to a printable issue form, the constitutional mechanism it belongs to, a website destination, and the imagery direction. Machine-readable data lives in [\`ecosystem-apparel-catalog.json\`](ecosystem-apparel-catalog.json).\n\n## The four printable issue forms\n\n| Code | Issue form | Garment rule | Website role |\n|---|---|---|---|\n| PN | Public Notice | ${printRules.PN} | Direct observation; Regalia and future subject collections |\n| HW | House Warrant | ${printRules.HW} | Realm and the relevant Great House |\n| CO | Court & Order | ${printRules.CO} | Realm, peerage, institutions, and Orders |\n| RC | Royal Commemoration | ${printRules.RC} | Calendar, Lineage, and commemorative Regalia |\n\nAtmospheric photography follows [\`IMAGERY_DIRECTION.md\`](../brand/IMAGERY_DIRECTION.md). Print art is built first and remains separate from the photographic mockup. Public Notices never receive sovereign heraldry.\n\n## Collection-to-ecosystem map\n\n| Subject collection | Default House | Institution | Default form | Suggested garment field | Expansion concepts |\n|---|---|---|---|---|---:|\n${collectionRows}\n\nThe House assignment identifies the mechanism being satirized; it does not require a badge on the garment. A Public Notice may map to a House online while remaining lore-free on the shirt.\n\n## Founding Ten\n\nThese records remain authoritative over every expansion classification. Existing SVGs are editable prototypes; generated artwork plates are concept references until reconstructed or approved at provider resolution.\n\n| ID | Product | Collection | Form | House | Production record |\n|---|---|---|---|---|---|\n${foundingRows}\n\n## First expansion tranche\n\nThese twelve concepts deliberately test four Public Notices, four House Warrants, and four Court & Order treatments across the wider subject catalog. They are the recommended next designs after the Founding Ten; selection is creative prioritization, not clearance or approval for sale.\n\n| ID | Declaration | Subject collection | Form | House | Isolated artwork brief |\n|---|---|---|---|---|---|\n${priorityRows}\n\n## Production sequence\n\n1. Lock exact wording and issue form.\n2. Create or refine isolated front artwork; no garment or room.\n3. Test at 200 px for recognition and at provider dimensions for legibility.\n4. Convert approved artwork to an editable, separation-ready production master.\n5. Place that exact master on the provider template.\n6. Generate concept photography using the locked artwork as the reference.\n7. Order a physical sample; inspect placement, underbase, fine lines, color, fit, and wash behavior.\n8. Only then change commerce status or describe the item as available.\n\n## Expansion library\n\n${librarySections}\n\n## Catalog-wide acceptance rules\n\n- The observation must read before the lore.\n- One front print area at launch.\n- One hero object, recognizable in two seconds, when imagery is used.\n- Three short lines of primary text at most; longer provenance belongs online or in packaging.\n- Public Notices use no sovereign arms, supporters, or decorative crown.\n- House Warrant badges remain subordinate to the declaration.\n- Court and Commemoration designs may use ornate imagery only when the object is immediately recognizable.\n- English carries meaning; Latin is optional texture with a nearby translation online.\n- Generated artwork is never treated as print-ready solely because it looks finished.\n- Every item retains open rights, provider, sample, and commerce gates until those reviews are documented.\n`;

const json = `${JSON.stringify(catalog, null, 2)}\n`;
const checkOnly = process.argv.includes("--check");

if (checkOnly) {
  const stale = [
    [jsonPath, json],
    [markdownPath, markdown],
  ].filter(([file, expected]) => !fs.existsSync(file) || fs.readFileSync(file, "utf8") !== expected);
  if (stale.length) {
    console.error(`Catalog output is stale: ${stale.map(([file]) => path.relative(root, file)).join(", ")}`);
    process.exit(1);
  }
  console.log(`Checked ecosystem catalog: ${catalog.counts.uniqueProducts} unique concepts, outputs current.`);
} else {
  fs.writeFileSync(jsonPath, json);
  fs.writeFileSync(markdownPath, markdown);
  console.log(`Wrote ${path.relative(root, markdownPath)} and ${path.relative(root, jsonPath)} (${catalog.counts.uniqueProducts} unique concepts).`);
}
