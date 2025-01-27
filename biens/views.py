from django.shortcuts import render, redirect
from .forms import BienForm
from django.http import HttpResponse
from .forms import BienForm
from django.shortcuts import render, redirect
from .models import Bien
from .forms import BienForm

def create_bien(request):
    if request.method == 'POST':
        form = BienForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hello')  
    else:
        form = BienForm()
    return render(request, 'create_bien.html', {'form': form})
