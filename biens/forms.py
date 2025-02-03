from django import forms
from .models import Objet

class ObjetForm(forms.ModelForm):
    class Meta:
        model = Objet
        fields = ['name', 'categorie', 'montant', 'achat_at', 'document', 'photo']
  