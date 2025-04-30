# views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
from .models import Recette, Categorie, RecetteIngredientUnit
from django.db.models import Q

# Liste des recettes
class RecetteListView(ListView):
    model = Recette
    template_name = 'recettes/recette_list.html'
    context_object_name = 'recettes'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Recette.objects.filter(
                Q(titre__icontains=query) | Q(categorie__nom__icontains=query)
                | Q(ingredients__icontains=query) | Q(etapes__icontains=query)
                | Q(conseils__icontains=query) | Q(description__icontains=query)           
            )
        return Recette.objects.all().order_by('categorie__nom','titre','description')

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
                "qte_adjusted": round(ingredient_unit.qte * nombre_couverts, 2),
                "unit": ingredient_unit.unit,
                "description": ingredient_unit.description,
            }
            for ingredient_unit in recette.recette_ingredient_units.all()
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
                "qte_adjusted": round(ingredient_unit.qte * nombre_couverts, 2),
                "unit": ingredient_unit.unit,
                "description": ingredient_unit.description,
            }
            for ingredient_unit in self.object.recette_ingredient_units.all()
        ]
        
        context = self.get_context_data()
        context.update({
            "calcul_result": calcul_result,
            "nombre_couverts": nombre_couverts,
        })
        return self.render_to_response(context)

