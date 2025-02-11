from django.contrib import admin
from .models import Objet, Categorie, Rubrique
from .admin_forms import ObjetAdminForm

# class DocInline(admin.TabularInline):
#     model = Bien.document.through
#     fields = ('name', 'document_pdf_link')
#     readonly_fields = ('document_pdf_link',)
#     extra = 0


class ObjetAdmin(admin.ModelAdmin):
    form = ObjetAdminForm
    list_display = ('name',  'categorie', 'created_at', 'achat_at','montant', 'document', 'photo')
    list_filter = ('rubrique', 'categorie','piece', 'montant', 'achat_at', 'utilisateur', 'created_at')
    search_fields = ['name', 'montant', 'achat_at','piece']
    fields = ['name', 'rubrique', 'piece', 'categorie', 'achat_at', 'montant', 'document', 'photo','utilisateur', 'created_at']

    readonly_fields = ['utilisateur', 'created_at']
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si l'objet est nouveau
            obj.utilisateur = request.user
        # obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Objet, ObjetAdmin)

class CategorieAdmin(admin.ModelAdmin):
    search_fields = ['name',]
admin.site.register(Categorie, CategorieAdmin) 

class RubriqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'montant_assu')
    search_fields = ['name',]
admin.site.register(Rubrique, RubriqueAdmin) 

