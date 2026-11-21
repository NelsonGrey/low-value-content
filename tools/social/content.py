"""Hand-written social copy. Everything derivable from the repo (calendar, lineage, houses, product copy) is
generated in build_social.py; only text that has no other home lives here. Draft copy: review before posting."""

BASE_TAGS = ["#LowValueContent", "#RoyalHouseOfEngagement", "#AttentionEconomy"]
KIND_TAGS = {
    "principle": ["#SocialMediaHumor"],
    "house": ["#TechSatire"],
    "lineage": ["#InternetHistory"],
    "calendar": ["#OnThisDay"],
    "product": ["#TShirtDesign"],
    "photo": ["#TShirtDesign"],
    "plate": ["#BrandIdentity"],
    "intro": [],
}

# One dry follow-on line for each constitutional principle (index = principle number).
PRINCIPLE_TAGS = {
    1: "Mined daily. Replenished never.",
    2: "A mandate renewed with every tap.",
    3: "Accepted everywhere. Redeemable for very little.",
    4: "Titles are conferred by visibility and revoked by silence.",
    5: "Production continues regardless of demand.",
    6: "Inscrutable, benevolent, and subject to change without notice.",
    7: "Applied consistently to every dashboard.",
    8: "The classification is under review. The condition is not.",
    9: "A standing order of the court.",
    10: "Applied at scale.",
}

PREMISE_CAPTION = (
    "Official regalia for the attention economy.\n\n"
    "The Royal House of Engagement governs what you notice, what you produce, and what you cannot stop checking. "
    "Low Value Content is its purveyor: wearable observations on the systems, rituals, and small humiliations of online life.\n\n"
    "The court is now in session. Follow for the founding collection."
)
STATUS_CAPTION = (
    "A note from the Chancery.\n\n"
    "Low Value Content is in early product development. The current designs are working concepts, not products offered for sale. "
    "Final garments, colors, pricing, release timing, and availability depend on rights review, physical samples, supplier selection, and a successful test order.\n\n"
    "We will say so again whenever it changes."
)

PLATES = {
    "identity": ("Plate I · The founding arms", "The founding arms of the Royal House",
                 "A peacock, a parrot, and a shield of four notifications. Concept study.",
                 "Plate I. The founding arms of the Royal House of Engagement: a peacock, a parrot, and a shield of four notifications. A concept study in the House register. Much published, little said.",
                 "Heraldic identity board showing the peacock and parrot arms, a seal, a notification emblem, and a royal standard on aged paper."),
    "collection": ("Plate II · The founding wardrobe", "The founding wardrobe, as imagined",
                   "Five garments on mannequins, in the study. Concept study.",
                   "Plate II. The wardrobe of the Royal House, as imagined: heraldic arms, an appointment seal, a sovereign's lions, and a medal. A concept study, not product photography. Nothing here is offered for sale.",
                   "Five T-shirts on wooden mannequins in an old-world study, with folded shirts on a marble table below."),
    "packaging": ("Plate III · Ceremonial materials", "Ceremonial materials",
                  "A box, tissue, wax seal, hangtag, and appointment card. Concept study.",
                  "Plate III. The ceremonial materials of the Royal House: a gilt-stamped box, sealed tissue, a hangtag, and an appointment card. A concept study. Packaging details remain to be confirmed.",
                  "A navy box with gold foil arms, tissue sealed with red wax, a cream hangtag, an appointment card, and a folded black shirt on a walnut desk."),
}
PHOTO_CAPTIONS = {
    7:  ("Much Published, Little Said.", "The sovereign motto of the House, borne by a peacock and a parrot. A concept mockup of the founding collection. In development; not yet for sale."),
    8:  ("The Order of the Blue Check.", "Conferred for verified distinction without regard to what was verified. A concept mockup. In development; not yet for sale."),
    9:  ("The end of the world has been postponed.", "A commemorative issue for the disputed reign of Y2K the Almost. A concept mockup. In development; not yet for sale."),
    10: ("Patron Saint of Debugging.", "For the Feast of Saint Moth, observed each 9 September. A concept mockup. In development; not yet for sale."),
}

SEED = ["intro-premise", "intro-status", "plate-1-identity", "principle-01"]  # post before announcing the accounts
FIRST_MONTH_NOTE = "Seed these four before following anyone or announcing the account."
