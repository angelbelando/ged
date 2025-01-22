from django import forms
from .models import Bien, Doc, Photo

class DocForm(forms.ModelForm):
    class Meta:
        model = Doc
        fields = ['fichier']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class BienForm(forms.ModelForm):
    class Meta:
        model = Bien
        fields = ['name', 'rubrique', 'categorie', 'achat_at', 'document', 'photo']
  