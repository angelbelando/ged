from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from .models import Objet, Categorie, Rubrique
from .forms import ObjetForm  
from django.views.generic import ListView, DetailView
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
from django.db.models import Sum
import matplotlib.pyplot as plt
import base64



def generate_thumbnail(request, objet_id):
    objet = get_object_or_404(Objet, id=objet_id)
    doc = fitz.open(objet.document.path)
    page = doc.load_page(0)  # Charger la première page
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.thumbnail((200, 200))  # Redimensionner l'image
    thumbnail_io = BytesIO()
    img.save(thumbnail_io, format='JPEG')
    thumbnail_io.seek(0)
    return HttpResponse(thumbnail_io, content_type='image/jpeg')


def home(request):
    return render(request, 'home.html')

class TableauBordView(ListView):
    model = Objet
    template_name = 'tableau_bord.html'
    context_object_name = 'objets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Annoter les objets avec les sous-totaux par rubrique
        context['rubriques'] = Objet.objects.values('rubrique_id').annotate(total_montant=Sum('montant'))
        
        # Ajouter les noms des rubriques
        context['detail_rubriques'] = Rubrique.objects.filter(id__in=[r['rubrique_id'] for r in context['rubriques']])
        
        # Fusionner les sous-totaux et les noms des rubriques et montant_assu
        for rubrique in context['rubriques']:
            rubrique['name'] = next((r.name for r in context['detail_rubriques'] if r.id == rubrique['rubrique_id']), None)
            rubrique['montant_assu'] = next((r.montant_assu for r in context['detail_rubriques'] if r.id == rubrique['rubrique_id']), None)
        
        # Créer le graphique
        categories = [rubrique['name'] for rubrique in context['rubriques']]
        total_montant = [rubrique['total_montant'] for rubrique in context['rubriques']]
        montant_assu = [rubrique['montant_assu'] for rubrique in context['rubriques']]

        x = range(len(categories))

        plt.figure(figsize=(10, 5))
        plt.bar(x, total_montant, width=0.4, label='Montant consommé', color='red', align='center')
        plt.bar([p + 0.4 for p in x], montant_assu, width=0.4, label='Montant d\'assurance', color='green', align='center')
        plt.xlabel('Rubrique Assurance')
        plt.ylabel('Montant')
        plt.title('Répartition contrat assurance')
        plt.xticks([p + 0.2 for p in x], categories)
        plt.legend()

        # Sauvegarder le graphique dans un buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Ajouter le graphique au contexte
        # Encoder le graphique en base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        context['barchart'] = image_base64
        return context


class ObjetListView(ListView):
    model = Objet
    context_object_name = "objets"
    template_name = 'liste_objets.html'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Objet.objects.filter(name__icontains=query)
        return Objet.objects.all()
        
class ObjetDetailView(DetailView):
    model = Objet
    template_name = 'detail_objet.html'

