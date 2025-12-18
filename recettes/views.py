# views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Recette, Categorie, RecetteIngredientUnit
from django.db.models import Q
import re
from rapidfuzz import fuzz
# 
from django.http import HttpResponse
from django.views import View
from docx import Document
# Document word python-docx

# from docx.oxml.ns import qn
# from docx.oxml import OxmlElement
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
# Fonction pour générer le document .docx


# Nettoyer les unités en fonction de la quantité
def nettoyer_unite(texte, qte):
    remplacements = {
        '/s': 's' if qte > 1 else '',
        '/x': 'x' if qte > 1 else ''
    }
    for suffixe, remplacement in remplacements.items():
        texte = re.sub(rf'\b{re.escape(suffixe)}\b', remplacement, texte)
    return texte

def formatter_qte(qte):
    if qte == 0:
        return ""
    elif qte == int(qte):
        return str(int(qte))
    else:
        return str(round(qte, 1))


# Liste des recettes de nous
# modification

def convertir_unite(qte, unite):
    """Convertit automatiquement certaines unités vers une unité supérieure."""
    unite_base = unite.strip().lower()

    if unite_base in ["g", "gramme", "grammes"] and qte >= 1000:
        return qte / 1000, "kg"
    elif unite_base in ["ml", "millilitre", "millilitres"] and qte >= 1000:
        return qte / 1000, "L"
    elif unite_base in ["cl", "centilitre", "centilitres"] and qte >= 100:
        return qte / 100, "L"
    else:
        return qte, unite
NUTRITION_DATA = {
    "huile": {"kcal": 884, "lipides": 100, "glucides": 0, "proteines": 0},
    "beurre": {"kcal": 717, "lipides": 81, "glucides": 0.9, "proteines": 0.9},
    "farine": {"kcal": 364, "lipides": 1, "glucides": 76, "proteines": 10},
    "sucre": {"kcal": 400, "lipides": 0, "glucides": 100, "proteines": 0},
    "lait": {"kcal": 64, "lipides": 3.5, "glucides": 4.8, "proteines": 3.4},
    "œuf": {"kcal": 143, "lipides": 9.5, "glucides": 1, "proteines": 13},
    "riz": {"kcal": 360, "lipides": 0.8, "glucides": 79, "proteines": 7.1},
    "pomme de terre": {"kcal": 86, "lipides": 0.1, "glucides": 20, "proteines": 1.7},
    "carotte": {"kcal": 41, "lipides": 0.2, "glucides": 10, "proteines": 0.9},
    "tomate": {"kcal": 18, "lipides": 0.2, "glucides": 3.9, "proteines": 0.9},
    "poulet": {"kcal": 165, "lipides": 3.6, "glucides": 0, "proteines": 31},
    "porc": {"kcal": 242, "lipides": 14, "glucides": 0, "proteines": 27},
    "bœuf": {"kcal": 250, "lipides": 15, "glucides": 0, "proteines": 26},
    "saumon": {"kcal": 208, "lipides": 13, "glucides": 0, "proteines": 20},
    "pain": {"kcal": 265, "lipides": 3.2, "glucides": 49, "proteines": 9},
    "fromage": {"kcal": 350, "lipides": 28, "glucides": 2, "proteines": 22},
    "parmesan": {"kcal": 431, "lipides": 29, "glucides": 4.1, "proteines": 38},
    "roquette": {"kcal": 25, "lipides": 0.7, "glucides": 3.7, "proteines": 2.6},
    "basilic": {"kcal": 23, "lipides": 0.6, "glucides": 2.7, "proteines": 3.2},
    "tomates cerises": {"kcal": 18, "lipides": 0.2, "glucides": 3.9, "proteines": 0.9},
    "noisettes": {"kcal": 628, "lipides": 61, "glucides": 17, "proteines": 15},
    "citron": {"kcal": 29, "lipides": 0.3, "glucides": 9.3, "proteines": 1.1},
    "vinaigre balsamique": {"kcal": 88, "lipides": 0, "glucides": 17, "proteines": 0.5},
    "huile d'olive": {"kcal": 884, "lipides": 100, "glucides": 0, "proteines": 0},
    "champignon": {"kcal": 22, "lipides": 0.3, "glucides": 3.3, "proteines": 3.1},
    "courgette": {"kcal": 17, "lipides": 0.3, "glucides": 3.1, "proteines": 1.2},
    "aubergine": {"kcal": 25, "lipides": 0.2, "glucides": 5.9, "proteines": 1},
    "oignon": {"kcal": 40, "lipides": 0.1, "glucides": 9.3, "proteines": 1.1},
    "ail": {"kcal": 149, "lipides": 0.5, "glucides": 33, "proteines": 6.4},
    "crème fraîche": {"kcal": 292, "lipides": 30, "glucides": 3, "proteines": 2.4},
    "yaourt nature": {"kcal": 61, "lipides": 3.3, "glucides": 4.7, "proteines": 3.5},
}
# Génération du document .docx
def find_nutrition(ingredient):
    """Recherche la clé nutritionnelle correspondante"""
    ing = ingredient.lower()
    for key in NUTRITION_DATA.keys():
        if key in ing:
            return NUTRITION_DATA[key]
    return None
# Génération du document .docx


def generate_docx(recette, nombre_couverts=None):
    document = Document()

    # --- Mise en page ---
    section = document.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    sectPr = section._sectPr
    cols = parse_xml(
        r'<w:cols xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:num="2" w:space="720"/>'
    )
    sectPr.append(cols)

    styles = document.styles
    normal = styles['Normal']
    normal.font.name = 'Calibri Light'
    normal.font.size = Pt(10)
    normal.font.color.rgb = RGBColor(40, 40, 40)

    # --- Titre & Métadonnées ---
    title = document.add_paragraph(recette.titre)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.runs[0]
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 102, 204)

    nb_couv = nombre_couverts or recette.nombre_couverts
    document.add_paragraph(f"{recette.description or ''}")
    meta = document.add_paragraph(f"📂 {recette.categorie.nom if recette.categorie else 'Non spécifiée'} | 🍽️ {nb_couv} couverts")
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.runs[0].font.size = Pt(9)
    meta.runs[0].italic = True

    total = (recette.temps_preparation or 0) + (recette.temps_cuisson or 0)
    tps = document.add_paragraph(
        f"⏱️ Préparation : {recette.temps_preparation or 0} min | "
        f"Cuisson : {recette.temps_cuisson or 0} min | Total : {total} min"
    )
    tps.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tps.runs[0].font.size = Pt(9)
    document.add_paragraph("")

    # --- Image ---
    if recette.image and hasattr(recette.image, 'path'):
        try:
            run = document.add_paragraph().add_run()
            run.add_picture(recette.image.path, width=Inches(3))
            document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception:
            document.add_paragraph("(Image non disponible)").alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Ingrédients & calcul nutritionnel ---

    p_ing = document.add_paragraph("🥕 Ingrédients",  style='Heading 1')
    p_ing.runs[0].bold = True
    p_ing.runs[0].font.color.rgb = RGBColor(0, 102, 204)

    total_nutrition = {"kcal": 0, "lipides": 0, "glucides": 0, "proteines": 0}
    for ing in recette.recette_ingredient_units.all().order_by('ordre', 'id'):
        # conversion en float pour éviter les erreurs Decimal / float
        qte_base = float(ing.qte or 0)
        nb_ref = float(recette.nombre_couverts or 1)
        nb_couv_f = float(nombre_couverts or nb_ref)

        qte = qte_base / nb_ref * nb_couv_f
        qte, unite = convertir_unite(qte, ing.unit)
        qte_fmt = formatter_qte(qte)
        unite_fmt = nettoyer_unite(unite, qte)
        document.add_paragraph(f"• {qte_fmt} {unite_fmt} {ing.description}", style='List')

        # --- Calcul nutritionnel ---
        # nutri = find_nutrition(ing.description)
        # if nutri:
        #     poids = float(qte) if unite_fmt in ["g", "kg"] else 0.0
        #     if unite_fmt == "kg":
        #         poids *= 1000
        #     factor = poids / 100.0
        #     for k in total_nutrition:
        #         total_nutrition[k] += nutri[k] * factor

    # --- Saut de colonne ---
    document.add_paragraph()._element.append(parse_xml(r'<w:br xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:type="column"/>'))

    # --- Étapes ---
    p_et = document.add_paragraph("👨‍🍳 Étapes", style='Heading 1')

    p_et.runs[0].bold = True
    p_et.runs[0].font.color.rgb = RGBColor(0, 102, 204)

    if recette.etapes:
        for ligne in recette.etapes.splitlines():
            txt = ligne.strip()
            if not txt:
                continue
            if txt.startswith('-'):
                p = document.add_paragraph(txt[1:].strip(), style='Heading 4')
            else:
                p = document.add_paragraph(txt, style='List Bullet')
            p.paragraph_format.space_after = Pt(1)
    else:
        document.add_paragraph("Aucune étape spécifiée.")

    # --- Tableau nutritionnel (joli) ---
    # if total_nutrition["kcal"] > 0:
    #     document.add_paragraph("")
    #     doc_table_title = document.add_paragraph("🍎 Valeurs nutritionnelles estimées (pour 1 portion)")
    #     doc_table_title.runs[0].bold = True
    #     doc_table_title.runs[0].font.color.rgb = RGBColor(0, 102, 204)

    #     table = document.add_table(rows=1, cols=2)
    #     table.style = 'Light List Accent 1'
    #     hdr_cells = table.rows[0].cells
    #     hdr_cells[0].text = "Élément"
    #     hdr_cells[1].text = "Valeur"

    #     for k, v in total_nutrition.items():
    #         row_cells = table.add_row().cells
    #         row_cells[0].text = k.capitalize()
    #         if k == "kcal":
    #             row_cells[1].text = f"{v / nb_couv:.0f} kcal"
    #         else:
    #             row_cells[1].text = f"{v / nb_couv:.1f} g"

    # --- Conseils & Note ---
    document.add_paragraph("")
    document.add_heading("💡 Conseils", level=1)
    document.add_paragraph(recette.conseils or "")

    document.add_heading("⭐ Note", level=1)
    stars = "★" * int(recette.note) + "☆" * (5 - int(recette.note))
    p = document.add_paragraph(stars)
    p.runs[0].font.color.rgb = RGBColor(255, 200, 0)

    # --- Ajustement police si trop long ---
    if len(document.paragraphs) > 85:
        for p in document.paragraphs:
            for run in p.runs:
                s = run.font.size.pt if run.font.size else 10
                run.font.size = Pt(max(9, s - 1))

    # --- Pied de page ---
    if not document.sections[0].footer.paragraphs:
        document.sections[0].footer.add_paragraph()
    footer = document.sections[0].footer.paragraphs[0]
    footer.text = "Document généré automatiquement par ABsite.fr"
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.runs[0].font.size = Pt(8)
    footer.runs[0].italic = True
    footer.runs[0].font.color.rgb = RGBColor(150, 150, 150)

    return document
class RecetteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recette
    template_name = 'recettes/recette_list.html'
    context_object_name = 'recettes'
    paginate_by = 20
    permission_required = 'recettes.view_recette'
    permission_denied_message = "Vous n'avez pas la permission de voir cette page."
    def get_queryset(self):
        query = self.request.GET.get('q')
        categorie_id = self.request.GET.get('categorie')
        qs = Recette.objects.all()

        # if query:
        #     qs = qs.filter(
        #         Q(titre__icontains=query) | Q(categorie__nom__icontains=query)
        #         | Q(ingredients__icontains=query) | Q(etapes__icontains=query)
        #         | Q(conseils__icontains=query) | Q(description__icontains=query)           
        #     )

        # if categorie_id:
        #     qs = qs.filter(categorie__id=categorie_id)

        # return qs.order_by('categorie__nom', 'titre', 'description')
        if query:
            qs = [r for r in qs if any([
                fuzz.partial_ratio(query.lower(), r.titre.lower()) > 80,
                fuzz.partial_ratio(query.lower(), r.ingredients.lower()) > 80,
                fuzz.partial_ratio(query.lower(), r.etapes.lower()) > 80,
                fuzz.partial_ratio(query.lower(), r.conseils.lower()) > 80,
                fuzz.partial_ratio(query.lower(), r.description.lower()) > 80,
                fuzz.partial_ratio(query.lower(), r.categorie.nom.lower()) > 80,
            ])]

        if categorie_id:
            qs = [r for r in qs if str(r.categorie.id) == str(categorie_id)]

        return sorted(qs, key=lambda r: (r.categorie.nom, r.titre, r.description))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all().order_by('nom')
        return context

# Détail une recette
class RecetteDetailView(DetailView):
    model = Recette
    template_name = 'recettes/recette_detail.html'
    context_object_name = 'recette'
    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recette = self.get_object()  # Récupère la recette en question

        # Utilisez le nombre de couverts du modèle pour l'affichage initial
        nombre_couverts = recette.nombre_couverts
        
        # Calcul des ingrédients ajustés
        
        calcul_result = [
            {
                "qte_adjusted": formatter_qte(round(ingredient_unit.qte/recette.nombre_couverts * nombre_couverts, 1)),
                "unit": ingredient_unit.unit,
                "description": ingredient_unit.description,
                "unit_display": nettoyer_unite(ingredient_unit.unit,round(ingredient_unit.qte/recette.nombre_couverts * nombre_couverts, 1)), # simple ajout d'un 's'
            }
            for ingredient_unit in recette.recette_ingredient_units.all().order_by('ordre','id')
        ]

        # Ajout au contexte
        context.update({
            "calcul_result": calcul_result,
            "nombre_couverts": nombre_couverts,
        })
        etapes = self.object.etapes.splitlines()
        context['etapes_formatees'] = [
        {'texte': e[1:].strip(), 'important': True} if e.strip().startswith('-') else {'texte': e.strip(), 'important': False}
        for e in etapes
        ]
        conseils = self.object.conseils.splitlines()
        context['conseils_formatees'] = [
        {'texte': c[1:].strip(), 'important': True} if c.strip().startswith('-') else {'texte': c.strip(), 'important': False}
        for c in conseils
        ]
    
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            nombre_couverts = int(request.POST.get('nombre_couverts', self.object.nombre_couverts))
            if nombre_couverts <= 0:
                raise ValueError("Le nombre de couverts doit être supérieur à zéro.")
        except (ValueError, TypeError):
            nombre_couverts = self.object.nombre_couverts
        
        calcul_result = [
            {
                "qte_adjusted": formatter_qte(round(ingredient_unit.qte/self.object.nombre_couverts * nombre_couverts, 1)),
                "unit": ingredient_unit.unit,
                "description": ingredient_unit.description,
                "unit_display": nettoyer_unite(ingredient_unit.unit,round(ingredient_unit.qte/self.object.nombre_couverts * nombre_couverts, 1)), # simple ajout d'un 's'
            }
            for ingredient_unit in self.object.recette_ingredient_units.all().order_by('ordre','id')
        ]
        
        context = self.get_context_data()
        context.update({
            "calcul_result": calcul_result,
            "nombre_couverts": nombre_couverts,
        })
        return self.render_to_response(context)

# Exporter une recette en fichier .docx
class ExportRecetteDocxView(View):
    def get(self, request, pk):
        recette = Recette.objects.get(pk=pk)
        # récupère le nombre de couverts depuis la requête
        try:
            nb_couv = int(request.GET.get('couverts', recette.nombre_couverts))
        except (TypeError, ValueError):
            nb_couv = recette.nombre_couverts

        document = generate_docx(recette, nombre_couverts=nb_couv)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{recette.titre}.docx"'
        document.save(response)
        return response
