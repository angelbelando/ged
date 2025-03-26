from django.contrib import admin
from .models import Document, TypeDocument

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document', 'rubrique', 'type_document', 'date_reference', 'Document_pdf','url', 'commentaire')
    list_filter = ('rubrique', 'type_document','date_reference')
    search_fields = ['document','commentaire', 'rubrique', 'date_reference']
    fields = ['document', 'rubrique', 'type_document', 'date_reference', 'Document_pdf','url', 'commentaire']
admin.site.register(Document, DocumentAdmin)

class TypeDocumentAdmin(admin.ModelAdmin):
    search_fields = ['name',]
admin.site.register(TypeDocument, TypeDocumentAdmin) 