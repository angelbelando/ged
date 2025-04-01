from django.contrib import admin
from .models import Recette, Favori, Note, Categorie


class CategorieAdmin(admin.ModelAdmin):
    search_fields = ['nom',]
admin.site.register(Categorie, CategorieAdmin) 

class RecetteAdmin(admin.ModelAdmin):
    search_fields = ['titre',]
admin.site.register(Recette, RecetteAdmin) 

class FavoriAdmin(admin.ModelAdmin):
    search_fields = ['recette',]
admin.site.register(Favori, FavoriAdmin) 

class NoteAdmin(admin.ModelAdmin):
    search_fields = ['recette',]
admin.site.register(Note, NoteAdmin) 