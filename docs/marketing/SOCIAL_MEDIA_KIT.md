# Social Media Kit

Status: draft, November 5, 2026. Everything here is a proposal for owner review. The accounts do not exist yet, and nothing has been posted. Nothing here claims trademark clearance; the brand guide's release model lists handle and name review as an open step.

This kit gives you what a new account needs on day one: profile images, bios, 58 ready-to-post graphics with captions and alt text, a posting calendar, and the rules for keeping the voice right. The graphics and the caption sheet are generated from the repo's own content (the manifest, the Calendar and Lineage copy, the approved product copy), so they stay in step with the site.

## What is in the kit

| File | What it is |
|---|---|
| `design/social/profile/avatar-1080.png` | Profile picture: the crowned notification mark inside a gold ring on navy. Survives a circular crop. |
| `design/social/profile/facebook-cover-1640x624.png` | Facebook cover. Lockup is centered so it survives the mobile crop. |
| `design/social/profile/linkedin-cover-1584x396.png` | LinkedIn page banner. |
| `design/social/feed/*.jpg` | 58 feed cards at 1080 x 1350 (4:5), the right shape for Instagram and Facebook feeds. |
| `design/social/posts.csv` | One row per card: suggested date, platforms, caption, hashtags, alt text, and a note for anything on hold. |
| `tools/social/` | The generator. `python3 tools/social/build_social.py` rebuilds everything (needs Pillow and Chrome, and the macOS system fonts). |

The 58 cards: 2 introductions, 3 concept plates, 10 constitutional principles, 6 Great Houses, 11 Lineage reigns, 12 Royal Calendar observances, 10 founding-collection designs, and 4 mannequin mockups.

## Ground rules

These come from [`LOW_VALUE_CONTENT_GUIDE.md`](../brand/LOW_VALUE_CONTENT_GUIDE.md) and apply to every post.

1. **Status first.** The designs are working concepts, not products for sale. No buy-now language, inventory claims, countdowns, ratings, reviews, or scarcity. Product posts say "In development; not yet for sale."
2. **Name the collection correctly.** Say "the founding collection." Do not use "Drop 001", "Founding Ten", or "Founding Plate" in public copy.
3. **Label concept imagery.** Mockups and plates are concept studies, not product photography. The cards and captions already say so; keep it when you edit.
4. **One observation per post:** the observation, the familiar scene behind it, accurate imagery, the true status, and one action.
5. **Never sound like a brand pretending to be a person.** No "link in bio!", no emoji pile-ons, no "hey fam". The House speaks as a serious institution.
6. **Target systems, not people.** No private individuals, protected groups, or vulnerable people. No other company's logos or trade dress.
7. **Do not call anything cleared, unique, or available.** The name and slogans are not trademark-cleared.

## Setting up the accounts

Do this once, before the first post.

- **Owner and sign-in.** Create everything under the company, not a personal account. Use `admin@nelsongrey.com` as the login, turn on two-factor authentication, and use `social@nelsongrey.com` as the public contact email. That is a role alias that delivers to `admin@`. Please confirm the alias exists. Do not use the personal Gmail or the Outlook billing address.
- **Order.** Create the Facebook Page first (in Meta Business Suite), then the Instagram professional account and link it to the Page, then LinkedIn. Hold TikTok until you have video (see below).
- **Name and handle.** Display name: **Low Value Content**. Try the handle `lowvaluecontent` first. Fall back to `lowvaluecontentco`. Consider also registering `royalhouseofengagement` so nobody else holds the House name. I have not checked availability on any platform.
- **Link.** Use whichever address is confirmed live. The README lists `https://low-value-content-prod.web.app` (currently the coming-soon page). The site config names `lowvaluecontent.com`, but I could not confirm that domain is owned and live.
- **Category.** Clothing (Brand) on Facebook and Instagram. Apparel and Fashion on LinkedIn.
- **Seed before you announce.** Post the first four cards (introduction, status note, Plate I, principle No. 1) before following anyone or inviting anyone. An empty account reads as abandoned and a seeded one reads as open.

### Bios (character counts checked)

| Platform | Limit | Text | Length |
|---|---|---|---|
| Instagram bio | 150 | Official regalia for the attention economy. The Royal House of Engagement, purveyed by Low Value Content. In development. | 121 |
| Facebook short description | 255 | Official regalia for the attention economy. Wearable observations on the systems, rituals, and small humiliations of online life, issued by the Royal House of Engagement. In early product development. | 200 |
| TikTok bio | 80 | Official regalia for the attention economy. In development. | 59 |
| LinkedIn tagline | 120 | Wearable observations on the systems and rituals of online life. In early product development. | 94 |

LinkedIn "About": use the brand foundation paragraph from the guide: *Low Value Content makes wearable observations about the systems, rituals, and small humiliations of online life. It is satire from inside the feed: written for people who participate in digital culture while remaining skeptical of what it rewards.* Then the current public status statement, word for word.

## Content pillars and cadence

| Pillar | Day | Cards | Notes |
|---|---|---|---|
| The Constitution | Monday | 10 principles | The most shareable cards. One line, no setup. |
| The Houses and the Lineage | Wednesday | 6 Houses, then 10 reigns | Good as carousels: post all six Houses as one swipe post. |
| The founding collection | Friday | 8 design cards and 3 mockups scheduled (2 held, see below) | Always "in development." |
| The Royal Calendar | On the real date | 12 observances (11 scheduled, 1 on hold) | The engine that never runs out: the cards post on their actual dates. |

Three posts a week on Instagram and Facebook, mirrored. LinkedIn only gets the cards that fit a work audience (introduction, status, principles, Houses, product cards), one or two a week, the next weekday after Instagram.

## The first 30 days

Suggested dates are in `design/social/posts.csv`, which has every caption. The first month:

| Date | Card | Platforms |
|---|---|---|
| Thu 5 Nov | `intro-premise` | Instagram, Facebook, LinkedIn |
| Fri 6 Nov | `intro-status` | Instagram, Facebook, LinkedIn |
| Sat 7 Nov | `plate-1-identity` | Instagram, Facebook |
| Sun 8 Nov | `principle-01` | Instagram, Facebook, LinkedIn |
| Mon 9 Nov | `principle-02` | Instagram, Facebook, LinkedIn |
| Wed 11 Nov | `house-01-prompt` | Instagram, Facebook, LinkedIn |
| Fri 13 Nov | `photo-07-much-published` | Instagram, Facebook |
| Mon 16 Nov | `principle-03` | Instagram, Facebook, LinkedIn |
| Wed 18 Nov | `house-02-scroll` | Instagram, Facebook, LinkedIn |
| Fri 20 Nov | `product-07-much-published` | Instagram, Facebook, LinkedIn |
| Mon 23 Nov | `principle-04` | Instagram, Facebook, LinkedIn |
| Wed 25 Nov | `house-03-influence` | Instagram, Facebook, LinkedIn |
| Fri 27 Nov | `product-01-validate` | Instagram, Facebook, LinkedIn |
| Mon 30 Nov | `calendar-11-30-day-of-artificial-eloquence` | Instagram, Facebook |
| Wed 2 Dec | `house-04-signal` | Instagram, Facebook, LinkedIn |
| Fri 4 Dec | `photo-09-y2k-the-almost` | Instagram, Facebook |

At three posts a week the kit lasts until about **24 February 2027**, plus the Calendar cards on their real dates through October 2027. Plan the next batch of material (the Wave 2 designs and new photography from `IMAGERY_DIRECTION.md`) before then.

## On hold, and what to review

The CSV marks these in its `note` column.

- **Hold: Blue Check device (4 cards).** The imagery log says the generic check device still needs a rights review. The cards that show it (`product-08`, `photo-08`, `lineage-04-emoticon`, and the 19 September Calendar card) are left unscheduled until that review is done.
- **Hold: No. 03 (1 card).** The `product-03` art is the weakest design; if you adopt the Duke of Doomscrolling redesign, regenerate that card.
- **Review: the 11 May Calendar card** names a real person (the chess match). Consider rewording for social.
- **All captions are draft copy.** The principle follow-on lines and the plate and mockup captions are mine; the rest come from the site and the product-copy draft, which is itself marked draft with open placeholders. Please read each caption once before it goes live.
- **Concept images:** the plates and mockups show designs that differ from the production art in places. Keep the "concept" wording.

## Platform notes

- **Instagram.** Post the cards at 4:5. Carousels work well for the Houses and the Lineage; put the cards in order and use the first as the cover. Paste the alt text from the CSV into the accessibility field. Keep hashtags to the five already listed.
- **Facebook.** Mirror Instagram. Facebook allows longer captions, so the full caption can go in as written.
- **LinkedIn.** Same cards, same captions, hashtags trimmed to three. Lean on the principles and Houses: the "work is content" angle.
- **TikTok.** There is no video in this kit, and a static card is the wrong format. Hold the account until you have a short-video plan. A swipe slideshow of the Houses or the Lineage can work in photo mode, but check the aspect ratio first (4:5 may be cropped).
- **Stories and Reels (9:16)** are not generated yet. They would be a straightforward addition to the generator.
- **Replies.** Dry, brief, and implicated, like the posts. Support questions get the calmer support voice from the guide: say what happened, the policy, and the next step. Never make the customer the joke.

## Regenerating

```sh
python3 tools/social/build_social.py            # everything
python3 tools/social/build_social.py --only house   # one family (ids start with the prefix)
```

Card copy that has no other home is in `tools/social/content.py`; layouts are in `tools/social/cards.py`. If the product copy, the Calendar, or the Lineage changes on the site, rerun the generator and the cards follow. The generator needs Chrome (set `CHROME` to use a different binary) and the Georgia and Snell Roundhand fonts that ship with macOS.

## Not done, and needs you

- Creating the accounts and confirming the handles, link, and `social@` alias.
- Reading and approving the captions.
- Scheduling. The scheduling connector (Postiz) is not authorized in this environment, and posting publicly needs your explicit go-ahead.
- Updating the website's Social page and footer links once real profile URLs exist. They currently point to a "plans" page.
- Video, Stories, and Wave 2 cards.
