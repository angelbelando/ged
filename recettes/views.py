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

# Fonction pour générer le document .docx
from django.shortcuts import get_object_or_404
from .utils.docx import generate_docx
from .utils.pdf import generate_pdf
from .utils.unit_renderer import nettoyer_unite, formatter_qte, convertir_unite
# from .renderers.docx_renderer import generate_docx
# from .renderers.pdf_renderer import generate_pdf
from django.utils.text import slugify
import io

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

        return sorted(qs, key=lambda r: (-r.date_publication.timestamp(), r.categorie.nom, r.titre, r.description))

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

class ExportRecettePDFView(View):
    def get(self, request, pk):
        recette = Recette.objects.get(pk=pk)
        # récupère le nombre de couverts depuis la requête
        try:
            nb_couvert = int(request.GET.get('couverts', recette.nombre_couverts))
        except (TypeError, ValueError):
            nb_couvert = recette.nombre_couverts

        buffer = io.BytesIO()
        generate_pdf(recette, buffer, nombre_couverts=nb_couvert)

        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="recette_{slugify(recette.titre)}.pdf"'
        return response