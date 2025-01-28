from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Objet
from .forms import ObjetForm  
from django.views import generic  

def create_objet(request):
    if request.method == 'POST':
        form = ObjetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hello')  
    else:
        form = ObjetForm()
    return render(request, 'create_objet.html', {'form': form})

class ObjetList(generic.ListView):
    model = Objet
    context_object_name = "objets"
    template_name = 'liste_objets.html'
    queryset = Objet.objects.all().select_related()
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context