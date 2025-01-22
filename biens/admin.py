from django.contrib import admin
from .models import Bien, Categorie, Photo, Doc

# class DocInline(admin.TabularInline):
#     model = Bien.document.through
#     fields = ('name', 'document_pdf_link')
#     readonly_fields = ('document_pdf_link',)
#     extra = 0


class BienAdmin(admin.ModelAdmin):
    list_display = ('name', 'rubrique', 'categorie', 'created_at', 'achat_at','montant', 'document', 'photo')
    list_filter = ('rubrique', 'categorie', 'montant', 'created_at', 'achat_at')
    search_fields = ['name','rubrique', 'categorie', 'montant', 'created_at', 'achat_at']
    # filter_horizontal = ("document","photo",)
admin.site.register(Bien, BienAdmin)

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ['name',]
admin.site.register(Photo, PhotoAdmin) 

class DocAdmin(admin.ModelAdmin):
    search_fields = ['name',]
admin.site.register(Doc, DocAdmin) 

class CategorieAdmin(admin.ModelAdmin):
    search_fields = ['name',]
admin.site.register(Categorie, CategorieAdmin) 

