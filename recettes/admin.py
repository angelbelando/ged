from django.contrib import admin
from .models import Recette, Categorie, RecetteIngredientUnit


class CategorieAdmin(admin.ModelAdmin):
    search_fields = ['nom',]
admin.site.register(Categorie, CategorieAdmin)

class RecetteIngredientUnitInline(admin.TabularInline):
    model = RecetteIngredientUnit  # Utilisez le modèle intermédiaire
    fields = ['qte', 'unit', 'description']  # Champs à afficher
    extra = 1

@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'temps_preparation', 'temps_cuisson', 'note')
    search_fields = ('titre', 'categorie__nom')
    fields = ('titre', 'description', 'categorie', 'temps_preparation', 'temps_cuisson', 'nombre_couverts',
              'ingredients', 'etapes', 'conseils', 'image', 'video_url_youtube', 'note', 'auteur')
    inlines = [RecetteIngredientUnitInline,]
