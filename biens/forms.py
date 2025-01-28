from django import forms
from .models import Objet, Doc, Photo

class DocForm(forms.ModelForm):
    class Meta:
        model = Doc
        fields = ['fichier']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class ObjetForm(forms.ModelForm):
    class Meta:
        model = Objet
        fields = ['name', 'rubrique', 'categorie', 'montant', 'achat_at', 'document', 'photo']
  