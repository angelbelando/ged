
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
from .models import Document


def hello(request):
    return render(request, 'Hello.html')

def generate_thumbnail(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    doc = fitz.open(document.Document_pdf.path)
    page = doc.load_page(0)  # Charger la première page
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.thumbnail((200, 200))  # Redimensionner l'image
    thumbnail_io = BytesIO()
    img.save(thumbnail_io, format='JPEG')
    thumbnail_io.seek(0)
    return HttpResponse(thumbnail_io, content_type='image/jpeg')

class DocumentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Document
    context_object_name = "documents"
    template_name = 'liste_documents.html'
    permission_required = 'documents.view_Document'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Document.objects.filter(
                Q(document__icontains=query) | Q(rubrique__icontains=query)
                | Q(commentaire__icontains=query)
            )
        return Document.objects.all().order_by('rubrique','document')
    
class DocumenttDetailView(DetailView):
    model = Document
    template_name = 'detail_document.html'