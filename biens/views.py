from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Objet
from .forms import ObjetForm  
from django.views.generic import ListView, DetailView

def create_objet(request):
    if request.method == 'POST':
        form = ObjetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hello')  
    else:
        form = ObjetForm()
    return render(request, 'create_objet.html', {'form': form})

class ObjetListView(ListView):
    model = Objet
    context_object_name = "objets"
    template_name = 'liste_objets.html'


class ObjetDetailView(DetailView):
    model = Objet
    template_name = 'detail_objet.html'