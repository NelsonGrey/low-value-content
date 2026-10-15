from pathlib import Path
from datetime import date
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "business-plan" / "Low_Value_Content_Business_Plan.docx"
CATALOG = ROOT / "docs" / "product" / "concept-catalog.md"
MOCKUP_1 = ROOT / "design" / "mockups" / "low-value-content-launch-01.png"
MOCKUP_2 = ROOT / "design" / "mockups" / "low-value-content-launch-02.png"
MOCKUP_3 = ROOT / "design" / "mockups" / "low-value-content-launch-03.png"

BLACK = "000000"
DARK = "263238"
MID = "56646B"
LIGHT = "EEF1F2"
PALE = "F7F8F8"
BORDER = "D9D9D9"
ACCENT = "8C6B4F"


def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcPr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_border(cell, color=BORDER, size="6"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = tcPr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tcPr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def set_cell_margins(cell, top=100, start=110, bottom=100, end=110):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tcMar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tcMar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)


def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)


def set_repeat_heading(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    keepNext = OxmlElement("w:keepNext")
    pPr.append(keepNext)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = " PAGE "
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    rel_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), rel_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "365F91")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rPr.extend([color, underline])
    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_para(doc, text="", style=None, bold_lead=None):
    p = doc.add_paragraph(style=style)
    if bold_lead and text.startswith(bold_lead):
        p.add_run(bold_lead).bold = True
        p.add_run(text[len(bold_lead):])
    else:
        p.add_run(text)
    return p


def add_bullets(doc, items, level=0):
    style = "List Bullet" if level == 0 else "List Bullet 2"
    for item in items:
        p = doc.add_paragraph(style=style)
        p.add_run(item)


def add_numbered(doc, items):
    for number, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.24)
        p.paragraph_format.first_line_indent = Inches(-0.24)
        p.paragraph_format.space_after = Pt(3)
        p.add_run(f"{number}.  {item}")


def add_table(doc, headers, rows, widths=None, numeric_cols=None, font_size=9.2):
    numeric_cols = set(numeric_cols or [])
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.style = "Table Grid"
    hdr = table.rows[0]
    set_repeat_table_header(hdr)
    prevent_row_split(hdr)
    for i, label in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_shading(cell, DARK)
        set_cell_border(cell)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(str(label))
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(font_size)
        if widths:
            cell.width = Inches(widths[i])
    for r_idx, row_data in enumerate(rows):
        row = table.add_row()
        prevent_row_split(row)
        for i, value in enumerate(row_data):
            cell = row.cells[i]
            set_cell_border(cell)
            set_cell_margins(cell)
            if r_idx % 2 == 1:
                set_cell_shading(cell, PALE)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in numeric_cols else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(value))
            run.font.size = Pt(font_size)
            if widths:
                cell.width = Inches(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


def page_break(doc):
    doc.add_page_break()


def parse_catalog(path):
    collections = []
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Collection"):
            current = {"name": line.replace("## ", "").strip(), "rows": []}
            collections.append(current)
        elif current and re.match(r"^\|\s*\d+\s*\|", line):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) >= 4:
                current["rows"].append(parts[:4])
    return collections


doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Inches(0.72)
section.bottom_margin = Inches(0.68)
section.left_margin = Inches(0.78)
section.right_margin = Inches(0.78)
section.header_distance = Inches(0.3)
section.footer_distance = Inches(0.3)

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(10.6)
styles["Normal"].font.color.rgb = RGBColor.from_string(BLACK)
styles["Normal"].paragraph_format.space_after = Pt(6)
styles["Normal"].paragraph_format.line_spacing = 1.08

styles["Title"].font.name = "Aptos Display"
styles["Title"].font.size = Pt(30)
styles["Title"].font.bold = True
styles["Title"].font.color.rgb = RGBColor.from_string(BLACK)
styles["Title"].paragraph_format.space_after = Pt(12)

for style_name, size, before, after in (("Heading 1", 19, 14, 7), ("Heading 2", 14, 10, 5), ("Heading 3", 11.5, 8, 4)):
    st = styles[style_name]
    st.font.name = "Aptos Display"
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor.from_string(BLACK)
    st.paragraph_format.space_before = Pt(before)
    st.paragraph_format.space_after = Pt(after)
    st.paragraph_format.keep_with_next = True

for list_style in ("List Bullet", "List Bullet 2", "List Number"):
    styles[list_style].font.name = "Aptos"
    styles[list_style].font.size = Pt(10.4)
    styles[list_style].paragraph_format.space_after = Pt(3)

if "Caption Clean" not in [s.name for s in styles]:
    cap = styles.add_style("Caption Clean", WD_STYLE_TYPE.PARAGRAPH)
    cap.font.name = "Aptos"
    cap.font.size = Pt(8.8)
    cap.font.italic = True
    cap.font.color.rgb = RGBColor.from_string(MID)
    cap.paragraph_format.space_before = Pt(3)
    cap.paragraph_format.space_after = Pt(8)

header = section.header.paragraphs[0]
header.text = "LOW VALUE CONTENT    BUSINESS PLAN"
header.style = styles["Normal"]
header.runs[0].font.size = Pt(8)
header.runs[0].font.bold = True
header.runs[0].font.color.rgb = RGBColor.from_string(MID)
header.paragraph_format.space_after = Pt(0)
footer = section.footer.paragraphs[0]
add_page_number(footer)
footer.runs[0].font.size = Pt(8)
footer.runs[0].font.color.rgb = RGBColor.from_string(MID)

# Cover
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(75)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("LOW VALUE CONTENT")
r.font.name = "Aptos Display"
r.font.size = Pt(13)
r.bold = True
r.font.color.rgb = RGBColor.from_string(ACCENT)
r.font.letter_spacing = Pt(2) if hasattr(r.font, "letter_spacing") else None

title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.add_run("Low Value Content Business Plan")

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_after = Pt(22)
sr = subtitle.add_run("Social media satire apparel launch and validation plan")
sr.font.size = Pt(15)
sr.font.color.rgb = RGBColor.from_string(MID)

if MOCKUP_1.exists():
    picp = doc.add_paragraph()
    picp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    picp.add_run().add_picture(str(MOCKUP_1), width=Inches(6.7))

meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.paragraph_format.space_before = Pt(18)
mr = meta.add_run("Prepared September 28 2026\nWorking business plan for founder review")
mr.font.size = Pt(10)
mr.font.color.rgb = RGBColor.from_string(MID)

page_break(doc)

# Executive summary
doc.add_heading("Executive Summary", level=1)
add_para(doc, "Low Value Content is a proposed direct to consumer apparel brand built around concise satire of social media, creator culture, workplace performance, algorithmic validation, doomscrolling, and artificial authenticity. The concept is easy to imitate at the product level. Its commercial case therefore depends on unusually strong writing, a consistent editorial design system, disciplined product quality, and an audience that returns for new releases.")
add_para(doc, "Current marketplace evidence supports a low cost test. Etsy has active demand for adjacent creator, algorithm, doomscrolling, and LinkedIn humor shirts, including listings with hundreds or thousands of reviews. The same evidence also shows crowded competition and frequent discounting. A six design print on demand launch is justified; a large inventory purchase, custom mobile application, or fifty design production run is not yet justified.")
add_para(doc, "The recommended first offer is a premium heavyweight Comfort Colors 1717 shirt at 32 dollars plus shipping, fulfilled through print on demand. Under the planning assumptions in this document, each Shopify order contributes about 18.98 dollars before monthly platform cost, advertising, refunds, samples, design labor, and income tax. The business remains attractive when customer acquisition stays below about 10 dollars. It becomes marginal when each sale requires 15 to 20 dollars in paid advertising.")

doc.add_heading("Launch Decision", level=2)
add_table(doc,
          ["Decision area", "Recommendation", "Reason"],
          [
              ["Initial assortment", "Six shirts", "Tests the voice without diluting attention across fifty listings"],
              ["Production", "Print on demand", "Avoids size and design inventory risk"],
              ["Primary garment", "Comfort Colors 1717", "Premium weight and finish support the intended positioning"],
              ["Price", "$32 plus shipping", "Provides room for product cost and modest acquisition spending"],
              ["Store", "Mobile friendly web store", "A native application adds cost without proven repeat usage"],
              ["Expansion", "Release winners in drops", "Moves investment toward demonstrated demand"],
          ], widths=[1.45, 1.65, 3.65])

doc.add_heading("Conditions for Continued Investment", level=2)
add_bullets(doc, [
    "At least 25 to 50 purchases from customers outside the founders personal network during the first four weeks.",
    "Two or more designs show demand so the result is not dependent on one accidental winner.",
    "Store conversion reaches roughly 2 percent or better after traffic quality is reviewed.",
    "Customer acquisition cost remains below 10 dollars and contribution after marketing remains above 8 to 10 dollars per shirt.",
    "Samples and customer feedback confirm that the garment and print feel justify premium pricing.",
])

page_break(doc)

# Company concept
doc.add_heading("Company Concept", level=1)
doc.add_heading("Brand Name", level=2)
add_para(doc, "The working brand name is Low Value Content. The name functions as criticism of low quality online material and as self aware commentary on the shirt itself. A preliminary web search found no obvious exact apparel collision, and The domain lowvaluecontent.com was registered on October 15 2026. Neither the web search nor owning the domain constitutes trademark clearance.")

doc.add_heading("Positioning", level=2)
add_para(doc, "The brand targets people who participate in online culture while remaining skeptical of its incentives. The humor should criticize platform behavior, corporate performance, creator economics, and compulsive consumption. It should not depend on attacking individual users or protected groups.")
add_para(doc, "The proposed visual language uses neutral heavyweight garments, one color printing, editorial typography, restrained interface references, and small brand details. This system distinguishes the collection from novelty shirts that rely on loud clip art, generic templates, and isolated jokes.")

doc.add_heading("Working Brand Promise", level=2)
add_para(doc, "Low Value Content publishes wearable observations about online life. Each release should be specific enough to feel recognized, concise enough to read at a glance, and designed well enough to be worn after the joke is understood.")

doc.add_heading("Product Principles", level=2)
add_bullets(doc, [
    "The joke must work without a product description.",
    "The design must look intentional even when the viewer does not read every word.",
    "The shirt must feel like apparel rather than promotional merchandise.",
    "The collection must use a consistent voice without repeating the same joke structure.",
    "Platform names, logos, interface elements, and third party trade dress require additional review.",
])

doc.add_heading("Initial Audience", level=2)
add_table(doc,
          ["Audience", "Relevant tension", "Likely message fit"],
          [
              ["Professionals and managers", "Required participation in workplace posting and personal branding", "Social Media Theater"],
              ["Creators and marketers", "Dependence on engagement systems they also criticize", "Creator Economy and Algorithm Anxiety"],
              ["Technology workers", "Awareness of platform mechanics and automated content", "Artificial Authenticity"],
              ["Chronically online consumers", "Humor about attention, notifications, and doomscrolling", "Chronically Online"],
              ["Gift buyers", "Need for specific occupational or personality humor", "Best selling individual statements"],
          ], widths=[1.55, 3.0, 2.2])

page_break(doc)

# Market
doc.add_heading("Market Assessment", level=1)
doc.add_heading("Evidence of Adjacent Demand", level=2)
add_para(doc, "The available evidence shows a market for adjacent products rather than proof of demand for this exact brand. Etsy reported 86.5 million active buyers, 5.6 million active sellers, and more than 100 million items for sale at the end of 2025. Apparel was among its six largest merchandise categories. Etsy also reported that custom or made to order merchandise represented about 30 percent of marketplace gross merchandise sales.")
add_para(doc, "Marketplace searches show more than 1,000 content creator shirt results and roughly 491 algorithm shirt results. Visible examples commonly sell between about 17 and 35 dollars. Several listings have hundreds or thousands of reviews. Doomscrolling and LinkedIn satire listings also show triple digit review counts. These signals support a launch test, but they also reveal a saturated market with heavy discounting and weak barriers to entry.")

doc.add_heading("Competitive Structure", level=2)
add_table(doc,
          ["Competitor type", "Strength", "Weakness", "Response"],
          [
              ["Etsy POD sellers", "Search traffic and low prices", "Inconsistent identity and quality", "Use a coherent brand and premium samples"],
              ["Redbubble and marketplace artists", "Large catalogs and easy discovery", "Commodity presentation and limited customer relationship", "Build owned email and website traffic"],
              ["Corporate humor brands", "Clear occupational audience", "Often broad and generic", "Stay specific to online behavior"],
              ["Creator merchandise", "Existing audience and trust", "Usually attached to one personality", "Build an editorial voice that supports many contributors"],
              ["Fast copycat sellers", "Rapid imitation and discounting", "Weak originality and customer loyalty", "Release often and protect core brand assets"],
          ], widths=[1.35, 1.65, 1.7, 2.05])

doc.add_heading("Market Conclusion", level=2)
add_para(doc, "Low Value Content has a plausible niche because the subject is culturally current, apparel purchases already occur around adjacent jokes, and print on demand keeps the test inexpensive. The opportunity is unsuitable for a large initial investment because competitors can copy short sayings and because customer acquisition costs can absorb most of the margin. The business should proceed as a measured brand experiment with explicit stop and scale criteria.")

doc.add_heading("Differentiation Requirements", level=2)
add_bullets(doc, [
    "A recognizable editorial voice across every release.",
    "Stronger garments and print quality than commodity novelty shirts.",
    "A consistent visual system that remains flexible across ten collections.",
    "Fast publication of new observations tied to online behavior without chasing every temporary meme.",
    "Owned customer relationships through the website and email rather than total marketplace dependence.",
])

# Product portfolio and mockups
doc.add_heading("Product Portfolio", level=1)
doc.add_heading("Ten Collections", level=2)
add_table(doc,
          ["Collection", "Subject", "Example"],
          [
              ["Social Media Theater", "Posting, promotions, thought leadership, and public performance", "Thought leader No thoughts required"],
              ["Algorithm Anxiety", "Engagement, recommendation systems, validation", "Please validate me algorithmically"],
              ["Creator Economy", "Monetization, personal brands, content production", "Content creator Meaning pending"],
              ["Chronically Online", "Doomscrolling, notifications, attention", "I am not doomscrolling I am doing market research"],
              ["Artificial Authenticity", "AI content, edited vulnerability, simulated sincerity", "Authenticity now available as a service"],
              ["Future of Work", "AI, automation, humanoid robots, and employment hype", "Your replacement is currently rebooting"],
              ["Productivity Theater", "Meetings, hustle, efficiency, and visible busyness", "Busy is my core competency"],
              ["Performative Sustainability", "Greenwashing, energy contradictions, and corporate virtue", "Carbon neutral PowerPoint"],
              ["Terms and Conditions", "Subscriptions, privacy, apps, and digital ownership", "Basic personality Premium features"],
              ["Optimized Human", "Wellness, self tracking, and compulsory self improvement", "Mindfulness but competitively"],
          ], widths=[1.55, 3.0, 2.2], font_size=8.3)

doc.add_heading("Ten Featured Shirt Examples", level=2)
add_para(doc, "The first six remain the recommended validation assortment. Four additional examples demonstrate how the design system extends into the newer collections without requiring all ten shirts to enter production at launch.")
add_numbered(doc, [
    "Please validate me algorithmically.",
    "Thought leader. No thoughts required.",
    "I am not doomscrolling. I am doing market research.",
    "Content creator. Meaning pending.",
    "My authentic self is currently being monetized.",
    "I optimized this shirt for engagement.",
    "Your replacement is currently rebooting.",
    "Busy is my core competency.",
    "Basic personality. Premium features.",
    "Mindfulness, but competitively.",
])

if MOCKUP_1.exists():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(MOCKUP_1), width=Inches(6.8))
    cp = doc.add_paragraph("Concept mockups for the first three launch designs", style="Caption Clean")
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
if MOCKUP_2.exists():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(MOCKUP_2), width=Inches(6.8))
    cp = doc.add_paragraph("Concept mockups for the companion three launch designs", style="Caption Clean")
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
if MOCKUP_3.exists():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(MOCKUP_3), width=Inches(6.8))
    cp = doc.add_paragraph("Four expansion examples from the extended collection matrix", style="Caption Clean")
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_para(doc, "The mockups illustrate the intended garment, color, and typography system. They are not production artwork. Final files require licensed fonts, outlined text, printer specific dimensions, color specifications, and sample approval.")

page_break(doc)

# IP
doc.add_heading("Intellectual Property and Brand Protection", level=1)
doc.add_heading("What the Business Can Protect", level=2)
add_para(doc, "The strongest protectable asset is the Low Value Content brand as a source identifier for clothing and related goods. A federal intent to use trademark application may be filed before launch if a comprehensive clearance search supports the name. Registration requires later evidence of genuine commercial use.")
add_para(doc, "Original human authored illustrations and sufficiently creative graphic compositions can receive copyright protection. The Copyright Office generally does not protect names, slogans, short phrases, ideas, familiar symbols, or basic typography. Individual shirt sayings will therefore be difficult to own exclusively even when the business creates them independently.")

doc.add_heading("Required Protection Steps", level=2)
add_numbered(doc, [
    "Complete a comprehensive search for Low Value Content and confusingly similar marks across federal, state, business name, domain, social, and marketplace records.",
    "Register the domain and relevant social handles, but delay a major public launch until name clearance is complete.",
    "Use the brand on neck labels, hangtags, packaging, receipts, and storefront materials so it functions as a source identifier rather than only as decoration.",
    "Use the trademark symbol while claiming the brand and reserve the registration symbol for a federally registered mark.",
    "Keep dated drafts, source files, artist briefs, invoices, licenses, and publication records.",
    "Require contractors to assign relevant artwork and usage rights in writing.",
    "Register important human authored visual works when their commercial value justifies the cost.",
])

doc.add_heading("Specific Risks", level=2)
add_table(doc,
          ["Risk", "Why it matters", "Control"],
          [
              ["Ornamental trademark refusal", "Large front text may be viewed as decoration rather than branding", "Use Low Value Content on labels, packaging, and consistent source identifying locations"],
              ["Third party platform marks", "Names, logos, colors, and interface trade dress may imply affiliation", "Use commentary carefully and avoid copied logos or exact interface reproduction"],
              ["Phrase collision", "Short jokes may have prior commercial use", "Search exact wording, variants, marketplaces, and trademark records before production"],
              ["AI authorship limits", "Purely generated artwork may lack copyright protection", "Use substantial human selection, arrangement, drawing, and revision"],
              ["Copycats", "Successful sayings can be reproduced quickly", "Compete through release cadence, customer relationship, garment quality, and brand recognition"],
          ], widths=[1.45, 2.75, 2.55])

# Model and operations
doc.add_heading("Business Model and Operations", level=1)
doc.add_heading("Recommended Sales Architecture", level=2)
add_para(doc, "The first launch should use a mobile friendly website connected to a print on demand provider. A native iOS application should wait until repeat purchase behavior or product drops create a clear reason for installation and push notifications.")
add_table(doc,
          ["Stage", "Store and fulfillment", "Purpose"],
          [
              ["Validation", "Printify Pop Up Store or Shopify with Printify", "Launch quickly without inventory"],
              ["Brand development", "Shopify with Apliiq or a controlled POD provider", "Improve labeling, packaging, analytics, and customer experience"],
              ["Proven designs", "Local screen printer plus stocked inventory", "Improve unit cost and print consistency"],
              ["Scale", "Hybrid stocked winners and POD long tail", "Preserve assortment while concentrating inventory on demand"],
          ], widths=[1.25, 2.75, 2.75])

doc.add_heading("Fulfillment Workflow", level=2)
add_numbered(doc, [
    "The customer selects the saying, garment color, and size.",
    "The storefront accepts payment and sends the order to the POD provider.",
    "The provider prints, packs, ships, and returns tracking information.",
    "The storefront sends shipment updates and handles customer communication according to the providers service model.",
    "Sales data identifies designs that qualify for bulk production.",
])

doc.add_heading("Garment and Print Standards", level=2)
add_bullets(doc, [
    "Primary blank: Comfort Colors 1717 or another verified heavyweight relaxed fit shirt.",
    "Initial printing: one color direct to garment for POD flexibility.",
    "Scaled printing: one or two color screen printing for proven designs.",
    "Initial palette: ivory, washed charcoal, stone, and muted gray green, subject to print testing.",
    "Every offered design and color combination must be sampled and washed at least three times before launch.",
])

doc.add_heading("Quality Review", level=2)
add_bullets(doc, [
    "Print alignment, opacity, edge quality, and placement.",
    "Collar shape, body length, shrinkage, and size consistency.",
    "Cracking, fading, or color migration after washing.",
    "Packaging, delivery time, and tracking quality.",
    "Correct neck branding and removal of unintended manufacturer labeling where promised.",
])

page_break(doc)

# Economics
doc.add_heading("Unit Economics", level=1)
doc.add_heading("Planning Assumptions", level=2)
add_table(doc,
          ["Input", "Assumption", "Basis"],
          [
              ["Garment", "Comfort Colors 1717", "Premium heavyweight positioning"],
              ["POD production", "$12.65", "Current Printify starting price"],
              ["POD shipping", "$3.99", "Current economy shipping starting price"],
              ["Retail price", "$32.00", "Premium but within visible adjacent market range"],
              ["Shipping charged", "$4.99", "Customer facing planning rate"],
              ["Shopify processing", "2.9% plus $0.30", "Current Basic plan standard online rate"],
              ["Shopify subscription", "$39 monthly", "Month to month Basic plan"],
          ], widths=[2.1, 1.7, 2.95], numeric_cols=[1])

doc.add_heading("Shopify POD Contribution", level=2)
add_table(doc,
          ["Line item", "Per order"],
          [
              ["Shirt revenue", "$32.00"],
              ["Shipping collected", "$4.99"],
              ["Total collected", "$36.99"],
              ["Shirt and printing", "($12.65)"],
              ["POD shipping", "($3.99)"],
              ["Payment processing", "($1.37)"],
              ["Contribution before overhead and marketing", "$18.98"],
          ], widths=[4.8, 1.4], numeric_cols=[1], font_size=9.5)

doc.add_heading("Monthly Platform Allocation", level=2)
add_table(doc,
          ["Monthly shirt sales", "Shopify cost per shirt", "Contribution after platform allocation"],
          [["10", "$3.90", "$15.08"], ["25", "$1.56", "$17.42"], ["50", "$0.78", "$18.20"], ["100", "$0.39", "$18.59"]],
          widths=[1.75, 2.15, 2.7], numeric_cols=[0, 1, 2])

doc.add_heading("Etsy POD Contribution", level=2)
add_table(doc,
          ["Line item", "Per order"],
          [
              ["Total collected", "$36.99"],
              ["Production and shipping", "($16.64)"],
              ["Etsy transaction fee", "($2.40)"],
              ["Estimated US payment processing", "($1.36)"],
              ["Listing renewal", "($0.20)"],
              ["Contribution before advertising", "$16.39"],
              ["Contribution after a 15% Offsite Ad fee", "$10.84"],
          ], widths=[4.8, 1.4], numeric_cols=[1], font_size=9.5)

doc.add_heading("Customer Acquisition Sensitivity", level=2)
add_table(doc,
          ["POD contribution", "Acquisition cost", "Remaining contribution"],
          [["$18.98", "$0", "$18.98"], ["$18.98", "$8", "$10.98"], ["$18.98", "$15", "$3.98"], ["$18.98", "$20", "($1.02)"]],
          widths=[2.1, 2.1, 2.2], numeric_cols=[0, 1, 2])

doc.add_heading("Bulk Production Economics", level=2)
add_para(doc, "Published 2026 examples place a one color Comfort Colors shirt around 13 to 14 dollars at 24 units and near 11 dollars around 96 units. Exact quotes depend on garment color, sizes, ink colors, print locations, setup, freight, and turnaround. Each saying is normally a separate print run, so ordering fifty units across six designs does not receive the same economics as three hundred identical shirts.")
add_para(doc, "Bulk production should begin only after sales identify repeatable winners. The principal financial benefit is a lower production cost. The principal financial risk is unsold inventory divided across designs, colors, and sizes.")

doc.add_heading("Costs Excluded From Contribution", level=2)
add_bullets(doc, [
    "Advertising, influencer compensation, affiliate commissions, and content production.",
    "Samples, photography, font licenses, design labor, and legal review.",
    "Refunds, replacements, chargebacks, and customer service time.",
    "Sales tax obligations, income tax, insurance, bookkeeping, and business registration.",
    "Discounts, bundles, free shipping differences, and costs for larger sizes or extra print locations.",
])

# Marketing
doc.add_heading("Marketing and Sales Plan", level=1)
doc.add_heading("Channel Priorities", level=2)
add_table(doc,
          ["Channel", "Role", "Initial approach"],
          [
              ["Owned website", "Primary brand and conversion destination", "Six products, clear fit and shipping information, email capture"],
              ["Instagram and TikTok", "Visual discovery and shareable satire", "Short observations, design reveals, customer wear shots"],
              ["LinkedIn", "Contextual distribution for workplace satire", "Use restrained posts that demonstrate the joke rather than imitate engagement bait"],
              ["Etsy", "Marketplace demand capture", "List selected proven designs and protect margin from fee stacking"],
              ["Email", "Repeat purchase and product drop channel", "Early access, voting, and release announcements"],
              ["Creator partnerships", "Credible access to aligned audiences", "Gift or affiliate arrangements with clear disclosure"],
          ], widths=[1.35, 2.25, 3.25])

doc.add_heading("Launch Content", level=2)
add_bullets(doc, [
    "A concise brand introduction that explains the target of the satire.",
    "One post for each launch saying showing the observation, design, and shirt.",
    "A comparison of the garment and print quality against ordinary novelty shirts.",
    "A customer vote on the next release from the remaining catalog.",
    "Behind the design material that shows human editing and authorship without overstating exclusivity.",
])

doc.add_heading("QR Code Product Experience", level=2)
add_para(doc, "A QR code on the upper back of every shirt can become a recognizable Low Value Content feature. The front should deliver a complete joke by itself. The QR code then rewards curiosity with a continuation, reveal, or small interaction before offering a restrained path to the store. This turns an observed shirt into a measurable discovery channel without making the garment feel like an advertisement.")
add_table(doc,
          ["Stage", "Customer experience", "Business role"],
          [
              ["Front of shirt", "A complete, readable setup or joke", "Earns attention without requiring a phone"],
              ["Back prompt", "A short invitation placed with the QR code", "Creates a reason to scan"],
              ["Joke page", "An immediate continuation, reveal, animation, or deliberately low value result", "Completes the interaction before selling"],
              ["Store path", "A discreet link to the featured shirt and broader collection", "Converts interest without interrupting the joke"],
          ], widths=[1.35, 3.05, 2.6], font_size=8.8)

doc.add_heading("Recommended Implementation", level=3)
add_bullets(doc, [
    "Assign each design a permanent URL on the owned domain, such as lowvaluecontent.com/q/doomscrolling, and place the printed short URL beneath the code as a fallback.",
    "Use a redirect controlled by Low Value Content so the destination can change after shirts have been printed without breaking the code.",
    "Show the joke continuation immediately. Do not require an app, account, email address, or extra permissions before the payoff.",
    "Track aggregate scans by design, campaign, and production batch while avoiding unnecessary personal data collection.",
    "Add the purchase link only after the continuation, with the scanned design preselected where practical.",
])

doc.add_heading("Print and Quality Requirements", level=3)
add_bullets(doc, [
    "Target an approximately 4 by 4 inch code on a relatively flat upper-back area, with strong contrast and a clear quiet zone around the code.",
    "Use a short destination URL so the generated pattern remains simple and tolerant of fabric texture, wrinkles, curvature, and normal print variation.",
    "Avoid seams, pockets, distressed treatments, gradients, ribbed fabric, and highly stretchable placements that can distort the modules.",
    "Test every garment color and print method while the shirt is flat, worn, wrinkled, stretched, and washed. Confirm scanning with several common phones and from realistic distances.",
    "Price the second print location before adoption. A back print can materially increase POD and bulk production cost, so the QR feature must be included in the unit economics and sample review.",
])

doc.add_heading("Example Experience", level=3)
add_para(doc, "Front: I am not doomscrolling. I am doing market research.", bold_lead="Front:")
add_para(doc, "Back prompt: View the findings", bold_lead="Back prompt:")
add_para(doc, "Scan result: Finding 1: Everyone is pretending this counts as work. Finding 2: You just scanned someone's shirt.", bold_lead="Scan result:")
add_para(doc, "A universal back prompt can also unify the catalog: This shirt contains additional low value content.")

doc.add_heading("Pricing Tests", level=2)
add_table(doc,
          ["Offer", "Purpose", "Caution"],
          [
              ["$32 plus shipping", "Baseline margin and transparent product price", "Shipping may reduce checkout conversion"],
              ["$36 delivered", "Simpler message and free shipping expectation", "Margin changes with destination"],
              ["Two shirt bundle", "Increase order value and distribute shipping cost", "Discount must preserve contribution"],
              ["Limited preorder", "Measure demand before bulk printing", "Communicate production and delivery dates clearly"],
          ], widths=[1.45, 2.65, 2.75])

# Roadmap
doc.add_heading("Launch Roadmap", level=1)
add_table(doc,
          ["Phase", "Timing", "Work", "Exit condition"],
          [
              ["Name and rights", "Week 1", "Trademark clearance, domain, handles, contractor terms", "Name approved for controlled use"],
              ["Product preparation", "Weeks 1 to 2", "Finalize six designs, choose fonts, order samples", "All samples pass visual and wash review"],
              ["Store preparation", "Weeks 2 to 3", "Build product pages, policies, analytics, email capture", "Test order completes successfully"],
              ["Soft launch", "Week 4", "Release to limited owned audience and collect feedback", "No critical quality or fulfillment defects"],
              ["Validation period", "Weeks 5 to 8", "Organic distribution and limited paid tests", "Meet or miss defined validation measures"],
              ["Scale decision", "End of week 8", "Select winners, revise pricing, request bulk quotes", "Documented continue, revise, or stop decision"],
          ], widths=[1.1, 1.05, 3.2, 2.0], font_size=8.8)

doc.add_heading("Validation Scorecard", level=2)
add_table(doc,
          ["Measure", "Target", "Interpretation"],
          [
              ["Non network purchases", "25 to 50", "Evidence that demand extends beyond friends and family"],
              ["Store conversion", "About 2% or better", "Review traffic quality before judging the site"],
              ["Customer acquisition cost", "Below $10", "Preserves useful contribution on a $32 shirt"],
              ["Contribution after marketing", "$8 to $10 or more", "Supports overhead and continued design work"],
              ["Design distribution", "At least two viable designs", "Reduces dependence on one accidental hit"],
              ["Quality defect rate", "Below 3%", "Signals whether the provider and artwork are reliable"],
              ["Return and replacement requests", "Below 5%", "Tests sizing communication and print quality"],
              ["Email opt in", "Track baseline", "Measures future release potential rather than one time sales only"],
          ], widths=[1.75, 1.55, 3.85], font_size=8.8)

doc.add_heading("Decision Rules", level=2)
add_bullets(doc, [
    "Continue when several designs sell, contribution remains positive after acquisition, and product feedback supports premium pricing.",
    "Revise when customers like the writing but object to garment quality, fit, shipping, or price.",
    "Stop or pause when sales rely on personal contacts, acquisition exceeds contribution, or one design accounts for nearly all demand without repeat interest.",
    "Move a design to bulk printing only after its sales history supports a size and color forecast.",
])

# Risks
doc.add_heading("Risk Register", level=1)
add_table(doc,
          ["Risk", "Likelihood", "Impact", "Mitigation"],
          [
              ["Crowded novelty apparel market", "High", "High", "Narrow voice, premium product, six design test"],
              ["Weak paid advertising economics", "High", "High", "Cap tests, track contribution, emphasize organic and partnerships"],
              ["Copied sayings and designs", "High", "Medium", "Protect brand, retain source files, publish consistently"],
              ["Trademark conflict", "Medium", "High", "Complete clearance before major investment"],
              ["POD quality variation", "Medium", "High", "Sample every offered variant and control providers"],
              ["Size and fit dissatisfaction", "Medium", "Medium", "Publish exact garment measurements and fit photographs"],
              ["Platform policy or account dependence", "Medium", "Medium", "Maintain owned domain, customer list, and exportable assets"],
              ["Humor becomes hostile or dated", "Medium", "Medium", "Use editorial review and retire weak designs"],
              ["Bulk inventory does not sell", "Medium", "High", "Use POD until design level demand is demonstrated"],
          ], widths=[1.75, 1.05, 0.95, 3.3], font_size=8.7)

doc.add_heading("Management Priorities", level=1)
add_numbered(doc, [
    "Clear the Low Value Content name and secure the domain before broader disclosure.",
    "Select the six launch sayings and complete exact phrase, marketplace, and trademark screening.",
    "Finalize licensed typography and one color production files.",
    "Order samples from at least two POD configurations and select the provider from physical evidence.",
    "Build the smallest store that supports a reliable purchase and fulfillment flow.",
    "Launch with explicit validation measures and record the result before adding products or inventory.",
])

# Appendix catalog
doc.add_heading("Appendix A Complete Saying and Design Catalog", level=1)
add_para(doc, "The following one hundred concepts are a creative working inventory. They have not received complete trademark, marketplace, or prior use clearance. Status labels indicate creative priority rather than legal approval.")
collections = parse_catalog(CATALOG)
for idx, coll in enumerate(collections):
    doc.add_heading(coll["name"], level=2)
    add_table(doc, ["No", "Saying", "Visual direction", "Status"], coll["rows"], widths=[0.45, 2.6, 3.35, 0.75], numeric_cols=[0, 3], font_size=8.2)
    if idx != len(collections) - 1:
        doc.add_paragraph()

# Appendix financial formulas
page_break(doc)
doc.add_heading("Appendix B Financial Model Notes", level=1)
doc.add_heading("Contribution Formula", level=2)
add_para(doc, "Contribution per order equals product revenue plus shipping revenue, less production, fulfillment shipping, payment processing, marketplace fees, refunds, discounts, and variable customer service costs. Monthly platform subscriptions and general operating expenses are deducted after unit contribution is calculated.")
doc.add_heading("Break Even Formula", level=2)
add_para(doc, "Monthly break even units equal fixed monthly operating cost divided by contribution per order. A 39 dollar Shopify subscription divided by 18.98 dollars of pre marketing contribution requires slightly more than two orders. This narrow calculation does not include design, legal, accounting, samples, advertising, or owner labor.")
doc.add_heading("Inventory Formula", level=2)
add_para(doc, "Inventory commitment equals the unit cost multiplied by the number of designs, colors, sizes, and units stocked. Six designs ordered at fifty units each create three hundred units of inventory even before a second color is added. Demand history should determine the size curve before bulk ordering.")

# Sources
doc.add_heading("Appendix C Sources and Research Notes", level=1)
sources = [
    ("United States Copyright Office Works Not Protected", "https://www.copyright.gov/help/faq/faq-protect.html"),
    ("United States Copyright Office Artificial Intelligence Copyrightability Report", "https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf"),
    ("United States Patent and Trademark Office Likelihood of Confusion", "https://www.uspto.gov/trademarks/search/likelihood-confusion"),
    ("United States Patent and Trademark Office Ornamental Refusal", "https://www.uspto.gov/trademarks/laws/ornamental-refusal-and-how-overcome-refusal-0"),
    ("United States Patent and Trademark Office Intent to Use Applications", "https://www.uspto.gov/trademarks/apply/intent-use-itu-applications"),
    ("Etsy 2025 Annual Report", "https://investors.etsy.com/sec-filings/all-sec-filings/content/0001370637-26-000019/etsy-20251231.htm"),
    ("Etsy Seller Fees", "https://help.etsy.com/hc/en-us/articles/115014483627-What-are-the-Fees-and-Taxes-for-Selling-on-Etsy"),
    ("Etsy Content Creator Shirt Search", "https://www.etsy.com/market/content_creator_t_shirt"),
    ("Etsy Algorithm Shirt Search", "https://www.etsy.com/market/algorithm_t_shirt"),
    ("Etsy LinkedIn Shirt Search", "https://www.etsy.com/market/linkedin_t_shirt"),
    ("Printify Comfort Colors 1717", "https://printify.com/app/products/706/comfort-colors/unisex-garmentdyed-tshirt"),
    ("Printify Bella Canvas Catalog", "https://printify.com/app/brand/7/bellacanvas"),
    ("Printify Shipping Options", "https://help.printify.com/hc/en-us/articles/4483626155409-What-are-Printify-s-shipping-options"),
    ("Printify Pop Up Store", "https://help.printify.com/hc/en-us/articles/12051129478417-What-is-Printify-Pop-Up-Store"),
    ("Shopify Pricing", "https://www.shopify.com/pricing"),
    ("Apliiq Print on Demand", "https://www.apliiq.com/print-on-demand"),
    ("Apple Developer Program Enrollment", "https://developer.apple.com/programs/enroll/"),
    ("Apple App Review Guidelines", "https://developer.apple.com/app-store/review/guidelines/uk/"),
    ("Cloudflare Registrar", "https://domains.cloudflare.com/"),
    ("RVA Threads Screen Printing Examples", "https://rvathreads.com/pages/screen-printing-price-examples"),
]
for label, url in sources:
    p = doc.add_paragraph(style="List Bullet")
    add_hyperlink(p, label, url)

doc.add_heading("Research Limitations", level=2)
add_para(doc, "Marketplace result counts, visible prices, provider costs, domain status, policies, and fees can change. Search results do not prove total sales, current availability, trademark clearance, or legal permission. The financial model uses starting prices and stated assumptions; actual quotes and completed test orders should replace those assumptions before launch. This document consolidates work completed through September 28 2026. It is a planning document, not legal, tax, accounting, investment, or market validation advice. Proposed requirements and projections should not be represented as completed implementation or achieved performance.")

doc.core_properties.title = "Low Value Content Business Plan"
doc.core_properties.subject = "Social media satire apparel launch and validation plan"
doc.core_properties.author = "Low Value Content"
doc.core_properties.comments = "Prepared from founder discussion and cited public sources through September 28 2026"

doc.save(OUT)
print(OUT)
