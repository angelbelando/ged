# views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Recette, Categorie, RecetteIngredientUnit
from django.db.models import Q
import re

def nettoyer_unite(texte,qte):
    # Supprime le '/s' s'il est collé à un mot ou entre deux mots
        texte_correct = texte
        if '/s' in texte and qte > 1:   # Si le texte contient '/s', on le remplace par 's' pour les pluriels
            texte_correct = re.sub(r'\b/s\b', 's', texte) 
        if '/x' in texte and qte > 1 :
             texte_correct = re.sub(r'\b/x\b', 'x', texte)  
        if '/s' in texte and qte == 1:
                # Si le texte contient '/s', on le remplace par 's' pour les pluriels
            texte_correct = re.sub(r'\b/s\b', '', texte)  
        if '/x' in texte and qte == 1 :
             texte_correct = re.sub(r'\b/x\b', '', texte)  
        return texte_correct


# Liste des recettes

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
            qs = qs.filter(
                Q(titre__icontains=query) | Q(categorie__nom__icontains=query)
                | Q(ingredients__icontains=query) | Q(etapes__icontains=query)
                | Q(conseils__icontains=query) | Q(description__icontains=query)           
            )

        if categorie_id:
            qs = qs.filter(categorie__id=categorie_id)

        return qs.order_by('categorie__nom', 'titre', 'description')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all().order_by('nom')
        return context

# Détail d'une recette
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
                "qte_adjusted": round(ingredient_unit.qte/recette.nombre_couverts * nombre_couverts, 1),
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
                "qte_adjusted": round(ingredient_unit.qte/self.object.nombre_couverts * nombre_couverts, 1),
                "unit": ingredient_unit.unit,
                "description": ingredient_unit.description,
                "unit_display": nettoyer_unite(ingredient_unit.unit,round(ingredient_unit.qte/recette.nombre_couverts * nombre_couverts, 1)), # simple ajout d'un 's'
            }
            for ingredient_unit in self.object.recette_ingredient_units.all().order_by('ordre','id')
        ]
        
        context = self.get_context_data()
        context.update({
            "calcul_result": calcul_result,
            "nombre_couverts": nombre_couverts,
        })
        return self.render_to_response(context)

