from django import forms
from .models import Recette

class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ['titre', 'description', 'ingredients', 'etapes', 'temps_preparation', 'temps_cuisson', 'categorie', 'image']
