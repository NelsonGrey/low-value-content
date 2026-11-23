# Voice review: is the site speaking as the Royal House of Engagement?

Status: review of **November 23, 2026**, covering every customer-facing page on `develop` (25 pages, about 6,300 words). Nothing here has been applied. Wording is judgment, not fact; the *Decisions for Mark* section at the end lists what needs a yes or no first.

## Verdict

The best pages already sound right. **Lineage, the Royal Calendar and the 404 page are firmly in the royal register**: sovereigns with epithets (*Moth the Pious*, *Spam the Unsolicited*), Latin mottos, feasts, a vigil, a coronation, "The Palace Regrets to Announce". Support ("Royal Office of Practical Matters", "plainly stated") is also right.

The problem is concentrated. The **Realm pages (Overview, Constitution, Great Houses)** are written as satire of a *modern constitutional state*: government, economy, legitimacy, ministries, portfolios, policy, committee, dashboards, data-driven. That is a Westminster register, not a medieval one, and it is the loudest mismatch because the Realm is where the world is explained. **About, Shop, Social and Cart** drift the same way, more mildly.

A vocabulary scan of the 14 story pages (hits in the page text):

| Group | Hits | Examples |
|---|---|---|
| Royal / medieval (target) | 168 | royal, realm, reign, peerage, court, crown, sovereign, regalia, feast, vigil, proclamation |
| Modern civic (breaks the frame) | 47 | constitution(al/ly) ×16, economy ×5, legitimacy ×4, government ×3, ministry/ministries ×4, policy, committee, portfolio |
| Modern corporate / data (breaks the frame) | 46 | reach, market research, monetized, revenue, data, dashboard, analytics, metrics, platform, drop |

Per page, the royal words outnumber the modern ones on Lineage (27 to 3), Calendar (20 to 2), Peerage (22 to 7) and the 404 (7 to 1). They are **outnumbered on Constitution (11 to 16) and Great Houses (15 to 17)** and roughly level on Realm Overview (19 to 13), About (4 to 5) and Cart (2 to 5).

## The rule (so the fixes stay consistent)

**A medieval court, solemnly governing modern things.** The joke works because the *institution* is old and the *subject* is new. So:

1. **Keep the modern thing's name.** The Algorithm, Scroll, Prompt, Spam, Buffer, doomscrolling, brain rot, the Blue Check. These are the subject of the satire; do not archaize them.
2. **Make the institution around it medieval.** Crown, realm, chancery, exchequer, heralds, court rolls, charter, writ, decree, levy, tithe, tally, fief, feast, vigil, fealty, estates. Avoid the vocabulary of a modern *state* (government, constitution, ministry, policy, economy, committee, portfolio, legitimacy) and of a modern *company* (industry, revenue, metrics, dashboard, platform, drop).
3. **Three tiers of dress.**
   - *Story pages* (Realm, Lineage, Calendar, About, Social, 404, product notes): full royal register.
   - *Shop and cart:* themed **headings and labels**, plain **instructions and money**. A customer must never have to decode what a button does or what they will pay.
   - *Legal and policy pages* (Terms, Privacy, Cookies, Shipping, Returns, Support body text): plain English. The page name and one eyebrow can be royal; the clauses must not be.
4. **The House takes itself seriously.** This is already the rule in `product-copy.md`: *the saying is the joke; the description never explains it; two sentences at most.*
5. **Printed text is a fixed point.** The approved shirt art prints "ROYAL INSTITUTE OF DIGITAL INQUIRY", "HOUSE OF SCROLL · FIELD WORK CONTINUES", "BY ALGORITHMIC APPOINTMENT", "OFFICIAL COURT APPOINTMENT · HONORARY". The site must not rename or contradict anything the garment prints.

### Word map

| Modern (avoid) | Royal (use) | Note |
|---|---|---|
| government | Crown, kingdom, the Court, the Household | "Government" reads as a civil state |
| constitution(al) | **Charter** (Magna Carta echo); "constitutions" in the plural is genuinely medieval (Clarendon, 1164) | Singular "The Constitution" reads American |
| economy | realm, wealth of the realm, trade, "the common purse" | |
| currency | coin of the realm | |
| industry | chief trade, craft, guild | |
| political legitimacy | right to rule | |
| aristocracy | nobility | |
| ministry / minister | exchequer, chancery, office, heralds, commission | "Ministry" as a department of state is 18th to 19th century |
| institute | college, office | "Institute" is a 19th century word, but see rule 5 |
| portfolio | charge (already your heraldic term: "six charges") | |
| committee | council, privy council | |
| policy | ordinance, decree, custom | |
| data-driven / metrics / analytics / dashboard | the tally, the reckoning, the audit, the rolls | Exchequers kept **tally sticks**; a perfect fit for the House of Signal |
| elected | anointed, crowned | |
| official designation | styled in the court rolls | |
| drop | issue | "Drop 001" is streetwear slang |
| holiday issue | Yuletide issue | |
| monetize | tax, levy, tithe | |
| platform-scale | of continental scale | |
| cart | the Royal Purse | heading only; keep "Checkout" plain |

## The Realm headline

Current: **"The government of attention."** Kicker: "By Sovereign Instrument". Lead: "The Crown *governs* the Attention Economy…"

Options, in my order of preference:

1. **The Kingdom of Attention.** Simple, instantly medieval, still a joke. *(Recommended.)*
2. The Crown's Dominion over Attention.
3. The Court of Attention.
4. Attention, by Divine Right. Funnier, but "divine right of kings" is early modern (17th century), so it only half passes your own test.

Suggested companions: kicker **By Royal Writ**; lead *"The Crown holds dominion over the realm's attention, turning attention into impressions, impressions into influence, and influence into proof of its own importance."*

## Findings, most important first

### Must fix (wrong, misleading, or customer-facing internal text)

| # | Where | Problem | Fix |
|---|---|---|---|
| M1 | Every product page, line under the price | These are **art-direction notes**, not copy: "with one Influence star and the punchline beneath the title", "No heraldry on the garment", "a descending feed beside the research excuse", "distinct status marks". They come from `regaliaRole` in `apparel-manifest.json`, which also feeds the ecosystem catalog. | Show the approved royal descriptions from `docs/product/product-copy.md` (already written). Keep `regaliaRole` for the catalog and add a separate customer field. Two lines need updating for the redesign (see below). |
| M2 | About, "The status" | "Low Value Content is **in product development**. Current designs, prices, specifications, and release timing remain **provisional** until rights review, physical sampling…" is pre-launch internal copy on a customer page; it contradicts a live store. "Final issues require physical sampling…" is an internal process. | Replace both paragraphs (draft below). Do not claim trademark clearance. |
| M3 | Thought Leader page | Credits the **"Ministry of Public Importance"**; the Great Houses page and the manifest call the same office the **"Chancery of Public Importance"**. The canon contradicts itself. (`apparel-manifest.json` line 217.) | Use **Chancery** everywhere. |
| M4 | Shipping and Returns | The eyebrow still reads **"Draft · November 23, 2026"** on a public policy page. (Mine; from #56.) | "Effective November 24, 2026" or similar once approved. |
| M5 | Peerage, "The permanent record" | Promises QR seals and that records are kept "in official packaging". No such packaging or routes exist. A claim the shop cannot yet keep. | Soften to what is true, or hold until it exists (draft below). |
| M6 | Privacy and Cookies | Public policy pages explain the **dev and staging Google sign-in gate**. Irrelevant to a customer, and the sign-in gate is not on production. | Remove those paragraphs from the production pages. |

### Should fix (breaks the register)

**Realm Overview** (`realm.astro`)

| Now | Proposed |
|---|---|
| The government of attention. | The Kingdom of Attention. |
| By Sovereign Instrument | By Royal Writ |
| The Crown *governs* the Attention Economy by converting… | The Crown holds dominion over the realm's attention, turning attention into impressions, impressions into influence, and influence into proof of its own importance. |
| A complete economy. Properly constituted. | A complete realm. Properly ordered. |
| Natural resource: Attention | The realm's wealth: Attention |
| Political legitimacy: Engagement | Right to rule: Engagement |
| Currency: Impressions | Coin of the realm: Impressions |
| Aristocracy: Influence | Nobility: Influence |
| Principal industry: Content | Chief trade: Content |
| Divine providence: The Algorithm | *(keep: already right)* |
| Known outside the court as Brain rot / Official designation: Sustained Cognitive Engagement | Known to the common folk as Brain rot / Styled in the court rolls: Sustained Cognitive Engagement |
| Three rooms. One government. | Three halls. One Crown. |
| Six permanent branches of government, each with a portfolio, an office and a contradiction | Six standing Houses, each with a charge, an office and a contradiction |

**The Constitution page** (`realm/constitution.astro`). Recommend renaming to **The Charter of Engagement** (keep the URL `/realm/constitution` or redirect it).

| Now | Proposed |
|---|---|
| The constitutional hierarchy / Authority descends. Responsibility does not. | The order of the realm / *(keep the second line: it is the best line on the page)* |
| 04 Ministries and Institutes: Convert prevailing conduct into policy, research, and administrative doctrine. | 04 Chanceries and Colleges: Convert prevailing conduct into decree, inquiry, and doctrine. |
| The doctrine of convenient evidence: **All decisions shall be data-driven.** All data shall be interpreted in accordance with the decision. | The doctrine of convenient evidence: **All decisions shall follow the tally.** All tallies shall be read in accordance with the decision. |
| Impressions are the currency. / Content is the principal industry. / Influence is the aristocracy. / Engagement is political legitimacy. | Impressions are the coin of the realm. / Content is the chief trade. / Influence is the nobility. / Engagement is the right to rule. |
| Metrics are presumed accurate until they become inconvenient. | Tallies are presumed accurate until they become inconvenient. |
| Brain rot is officially classified as sustained cognitive engagement. | Brain rot is styled in the court rolls as sustained cognitive engagement. |
| Current constitutional crisis: The Universal Peerage … *The matter was referred to committee.* | Current crisis of the realm: The Universal Peerage … *The matter was referred to the Privy Council.* |

**The Great Houses page** (`realm/houses.astro`; most strings in `apparel-manifest.json`)

| Now | Proposed |
|---|---|
| Six permanent branches of government, constitutionally equal, with a precedence that changes whenever the dashboard needs a better story. | Six standing Houses, equal by charter, with a precedence that changes whenever the tally needs a better story. |
| Equal by constitution. Ranked by convenience. | Equal by charter. Ranked by convenience. |
| House of Signal: "Analytics, dashboards, attribution, and evidence" | "Tallies, audits, reckonings, and evidence" |
| "Every decision is data-driven; the data is adjusted to support the decision." | "Every decision follows the tally; the tally is adjusted to support the decision." |
| Ministry of Measurable Outcomes | **Exchequer of Measurable Outcomes** (optional; see decisions) |
| Ministry of Universal Correspondence | **Heralds of Universal Correspondence** (optional) |
| The six charges identify the **portfolios** through which attention is produced… | …identify the **offices** through which attention is produced… |
| Royal Institute of Digital Inquiry | **Keep.** It is printed on shirt No. 03. |

**Peerage and Orders.** Mostly right (it is the strongest Realm page). Small changes: "Platform-scale compulsions" becomes "Compulsions of continental scale"; M5 above for the permanent-record block.

**About** (`about.astro`; page tone is closest to the Realm)

| Now | Proposed |
|---|---|
| A Brief Institutional History | A Brief Chronicle |
| …the institution charged with the orderly administration of attention. | …the House charged with keeping order over the realm's attention. |
| The work concerns systems and their incentives: platforms, institutions, metrics, markets… | The work concerns the powers and customs of the online realm: platforms, courts, tallies, and markets… |
| The status (M2) | **The issue.** *Six shirts, printed to order by our print partner and shipped across the United States. Sizes, colors, and prices are as listed. See Shipping and Returns for the terms.* (No mention of rights review or sampling.) |

**Homepage** (`index.astro`). The homepage is the storefront and must say what is sold. Recommend keeping the first line clear but dressing it:

| Now | Proposed |
|---|---|
| Shirts for the chronically online. | **Regalia for the chronically online.** (Still says what it is; "regalia" is already your word for the product.) |
| …governs the attention economy through six Great Houses… | …rules the realm of attention through six Great Houses, a line of sovereigns, and a calendar of feasts. |
| What you are buying | *(keep: product facts stay plain)* |

**Shop and product cards**

| Now | Proposed |
|---|---|
| Badge: Holiday issue | Yuletide issue |
| Public Notice cards show a modern genre line: "Algorithm Anxiety", "Creator Economy", "Artificial Authenticity" | "A Public Notice on Algorithm Anxiety" (same facts, royal frame) |
| Court & Orders cards show an institution (royal) | *(keep)* |

**Cart and order**

| Now | Proposed |
|---|---|
| Your cart | The Royal Purse (heading) |
| Order summary | The reckoning |
| Your cart is empty | The purse is empty |
| Checkout securely, Subtotal, Shipping, Tax, Estimated total, "Payment is handled by Stripe" | **Keep plain.** Money and trust copy must be unambiguous. |
| Order page: "Consulting the ledger…" | *(keep: already right)* |

**Social** (`social.astro`)

| Now | Proposed |
|---|---|
| "Official profile opens with Drop 001." | "…opens with the founding issue." |
| LinkedIn: "Work is content. Thought leadership, productivity theater, creator economics, and corporate performance…" | Keep the idea; reduce corporate nouns: "Work is content. The vanities of the working realm, handled carefully enough not to become what is being mocked." |

**Calendar and Lineage** (small)

| Now | Proposed |
|---|---|
| "Because history is easier to **monetize** when it occurs on the same date every year." | "Because history is easier to **tax** when it falls on the same date every year." |
| "Nineteen seconds became **an economy**." | "Nineteen seconds became **a guild**." |
| Lineage: "Neither **elected** nor understood" | "Neither **anointed** nor understood" |

### Product descriptions (M1): what to show

`product-copy.md` already has these. **Nos. 02, 03, 05, 06 can be used as written.** Nos. 01 and 04 describe the *old* art and need a light update:

| No. | Use | Note |
|---|---|---|
| 01 | A formal request for recognition, filed in the plain language of a public notice. Validation stands at three per cent; self-worth is pending. | Updated for the 3% redesign |
| 02 | An honorary court appointment, conferred without examination. The thoughts remain optional. | As written |
| 03 | Issued under the Royal Institute of Digital Inquiry, which has reclassified scrolling as fieldwork. | As written |
| 04 | An audit of the creator's affairs, returned with findings. The findings stand unamended. | Updated: the old line described an "editorial proof returned with comments" |
| 05 | An inventory tag for the self. Sponsorship is subject to terms. | As written |
| 06 | Two timestamps, entered into the record by the Ministry of Measurable Outcomes. The gap is one minute. | As written (rename with the Ministry decision) |

Also note: only Nos. 01, 02 and 05 show a Latin motto on their page; Nos. 03, 04 and 06 do not. Either add mottos (I would want the Latin checked by a person before it ships) or accept the inconsistency.

### Nice to have

- Lineage closing line "Until the next **platform update**" is a good punchline in a modern word; keep unless you want it fully royal ("Until the next Update").
- The legal pages could carry one royal eyebrow each ("Charter of Sale", "Notice of Privacy") with plain clauses beneath. Do not rewrite the clauses.
- `<title>` and meta descriptions follow the page headlines; update them with each rename so search results match.

## What is already right (leave alone)

The Lineage (all 11 reigns and their mottos), the Calendar entries and its Next observance block, the Support page, the 404, the Peerage worked example (*His Grace, the Duke of Doomscrolling*), "A note from the wardrobe", "Authority descends. Responsibility does not.", "Divine providence: The Algorithm", and the order page's "Consulting the ledger…".

## Decisions for Mark

1. **Realm headline.** *The Kingdom of Attention* (recommended), or another from the list above?
2. **Constitution becomes Charter?** Site-only rename; the URL can stay. Recommended yes.
3. **Rename the two Ministries** (Exchequer of Measurable Outcomes, Heralds of Universal Correspondence)? It also touches `product-copy.md`, the Great Houses page and the 06 product line. The Exchequer and tally-stick fit is strong. Recommended yes, but it is the most optional item here.
4. **Homepage headline.** *Regalia for the chronically online* (recommended) or keep the plain line?
5. **About page "The issue" paragraph.** Approve the wording, and tell me what you are comfortable saying about trademarks (nothing claiming clearance).
6. **Latin mottos** for Nos. 03, 04 and 06, or leave as is?

## How to apply (when approved)

Most Realm copy lives in `website/src/pages/realm*.astro` and in `docs/product/apparel-manifest.json` (houses, constitution, peerage, lineage, observances). Product descriptions need a new customer-facing field so the ecosystem catalog (which reads `regaliaRole`) is untouched. After any change run `python3 scripts/check-apparel-manifest.py`, `node scripts/build-ecosystem-catalog.mjs --check`, the build, and `cd tools/site-qa && npm run audit`.
