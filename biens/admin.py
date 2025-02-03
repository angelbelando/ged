from django.contrib import admin
from .models import Objet, Categorie, Rubrique

# class DocInline(admin.TabularInline):
#     model = Bien.document.through
#     fields = ('name', 'document_pdf_link')
#     readonly_fields = ('document_pdf_link',)
#     extra = 0


class ObjetAdmin(admin.ModelAdmin):
    list_display = ('name',  'categorie', 'created_at', 'achat_at','montant', 'document', 'photo')
    list_filter = ('rubrique', 'categorie', 'montant', 'created_at', 'achat_at')
    search_fields = ['name', 'categorie', 'montant', 'created_at', 'achat_at']
    # filter_horizontal = ("document","photo",)
admin.site.register(Objet, ObjetAdmin)



class CategorieAdmin(admin.ModelAdmin):
    search_fields = ['name',]
admin.site.register(Categorie, CategorieAdmin) 

class RubriqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'montant_assu')
    search_fields = ['name',]
admin.site.register(Rubrique, RubriqueAdmin) 

