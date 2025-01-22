from django.shortcuts import render, redirect
from .forms import BienForm
from django.http import HttpResponse
from .forms import BienForm


from django.shortcuts import render, redirect
from .forms import BienForm

def create_bien(request):
    if request.method == 'POST':
        form = BienForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hello')  # Remplace 'success_url' par l'URL de redirection souhaitée
    else:
        form = BienForm()
    return render(request, 'create_bien.html', {'form': form})


def hello(request):
    return HttpResponse('<h1>Hello Django! - success</h1>')
