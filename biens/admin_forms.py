from django import forms
from .models import Objet

class ObjetAdminForm(forms.ModelForm):
    class Meta:
        model = Objet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk and self.request:
            instance.utilisateur = self.request.user
        if commit:
            instance.save()
        return instance
