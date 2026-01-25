from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Frame, PageTemplate
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors

from .recette_renderer import build_recette_payload

def two_column_template(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(
        A4[0] / 2,
        1 * cm,
        "Document généré automatiquement par ABsite.fr"
    )
    canvas.restoreState()

def generate_pdf(recette, buffer, nombre_couverts=None):
    ctx = build_recette_payload(recette, nombre_couverts)

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1.3 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=1.3 * cm,
        rightMargin=1.3 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    title = ParagraphStyle(
        "title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        textColor=colors.HexColor("#0066cc"),
    )

    meta = ParagraphStyle(
        "meta",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=9,
        italic=True,
    )

    normal = styles["Normal"]
    normal.fontSize = 10

    h1 = ParagraphStyle(
        "h1",
        parent=styles["Heading1"],
        textColor=colors.HexColor("#0066cc"),
    )

    heading_ing = ParagraphStyle(
        "IngredientHeading",
        parent=styles["Heading4"],
        fontSize=10,
        spaceBefore=10,
        spaceAfter=4,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#0066cc"),
    )

    # --- Titre ---
    elements.append(Paragraph(ctx["titre"], title))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(ctx["description"], normal))
    elements.append(Spacer(1, 4))

    elements.append(
        Paragraph(
            f"{ctx['categorie']} | {ctx['nb_couverts']} couverts",
            meta,
        )
    )

    total = ctx["temps_preparation"] + ctx["temps_cuisson"]
    elements.append(
        Paragraph(
            f"Préparation : {ctx['temps_preparation']} min | "
            f"Cuisson : {ctx['temps_cuisson']} min | Total : {total} min",
            meta,
        )
    )

    elements.append(Spacer(1, 10))

    # --- Image ---
    if ctx["image"]:
        img = Image(ctx["image"], width=7 * cm, height=6 * cm)
        img.hAlign = "CENTER"
        elements.append(img)
        elements.append(Spacer(1, 10))

    # --- Ingrédients ---
    elements.append(Paragraph("Ingrédients", h1))
    for ing in ctx["ingredients"]:
        texte = ing["texte"]

        if texte.startswith(' --'):
            elements.append(Paragraph(texte.lstrip("- ").strip(), heading_ing))
        else:
            elements.append(Paragraph(f"• {texte}", normal))

    elements.append(Spacer(1, 12))

    # --- Saut de colonne ---
    elements.append(Spacer(1, 1))
    elements.append(Paragraph("<br/><br/>", normal))

    # --- Étapes ---
    elements.append(Paragraph("Étapes", h1))
    for et in ctx["etapes"]:
        style = styles["Heading4"] if et["type"] == "titre" else normal
        if et["type"] == "titre":
            elements.append(Paragraph(f"{et["texte"]}", heading_ing))
        else:
            elements.append(Paragraph(f"• {et['texte']}", style))

    # --- Conseils ---
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Conseils", h1))
    for con in ctx["conseils"]:
        style = styles["Heading4"] if con["type"] == "titre" else normal
        if con["type"] == "titre":
            elements.append(Paragraph(con["texte"], heading_ing))
        else:
            elements.append(Paragraph(con["texte"], normal))
    # --- Note ---
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Note", h1))
    stars = "★" * ctx["note"] + "" * (5 - ctx["note"])
    star_style = ParagraphStyle(
        "stars",
        parent=normal,
        textColor=colors.HexColor("#ffc800"),
        fontSize=14,
    )
    elements.append(Paragraph(stars, star_style))

    frame1 = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        (doc.width / 2) - 6,
        doc.height,
        id="col1",
    )
    frame2 = Frame(
        doc.leftMargin + (doc.width / 2) + 6,
        doc.bottomMargin,
        (doc.width / 2) - 6,
        doc.height,
        id="col2",
    )

    doc.addPageTemplates(
        [
            PageTemplate(
                id="TwoCol",
                frames=[frame1, frame2],
                onPage=two_column_template,
            )
        ]
    )

    doc.build(elements)




