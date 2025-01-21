from django.contrib import admin
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document', 'rubrique', 'mois', 'annee', 'Document_pdf','commentaire')
    list_filter = ('rubrique', 'mois', 'annee')
    search_fields = ['document','commentaire', 'rubrique', 'mois', 'annee']

admin.site.register(Document, DocumentAdmin)
