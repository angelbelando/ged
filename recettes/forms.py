from django import forms
from .models import Recette, RecetteIngredientUnit
# recettes/forms.py
from django.forms import inlineformset_factory


COMMON_INPUT_CLASS = "w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-gray-800 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
COMMON_TEXTAREA_CLASS = "w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-gray-800 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
COMMON_FORM_SELECT = "w-full rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-gray-800 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
FORM_CONTROL = (
    "w-full rounded-md border border-gray-300 "
    "px-3 py-1.5 text-sm "
    "shadow-sm "
    "focus:border-blue-500 focus:ring-1 focus:ring-blue-200"
)

class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette

      # fields = ['titre', 'description', 'ingredients', 'etapes', 'temps_preparation', 'temps_cuisson', 'categorie', 'image']
        fields = [
            "titre",
            "description",
            "categorie",
            "temps_preparation",
            "temps_cuisson",
            "nombre_couverts",
            "etapes",
            "conseils",
            "image",
            "video_url_youtube",
            "note",
        ]
        widgets = {
            "titre": forms.TextInput(attrs={"class": COMMON_INPUT_CLASS + " text-lg"}),
            "description": forms.Textarea(attrs={
                "class": COMMON_TEXTAREA_CLASS}),
            "etapes": forms.Textarea(attrs={
                "class": COMMON_TEXTAREA_CLASS}),
            "conseils": forms.Textarea(attrs={
                "class": COMMON_TEXTAREA_CLASS}),
            "categorie": forms.Select(attrs={
                "class": COMMON_FORM_SELECT,}),
            "nombre_couverts": forms.NumberInput(attrs={
                "class": COMMON_INPUT_CLASS,}),
            "temps_preparation": forms.NumberInput(attrs={
                "class": COMMON_INPUT_CLASS,}),
            "temps_cuisson": forms.NumberInput(attrs={
                "class": COMMON_INPUT_CLASS,}),
            "note": forms.Select(attrs={
                "class": COMMON_FORM_SELECT, }),
            "video_url_youtube": forms.Textarea(attrs={
                "class": COMMON_INPUT_CLASS, }),

        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = RecetteIngredientUnit
        fields = ["qte", "unit", "description", "ordre"]

        widgets = {
            "qte": forms.TextInput(attrs={
                "class": FORM_CONTROL}),
            "unit": forms.Select(attrs={
                "class": FORM_CONTROL,}),
            "description": forms.TextInput(attrs={
                "class": FORM_CONTROL,}),
            "ordre": forms.NumberInput(attrs={
                "class": "hidden",
            }),
        }

    ordre = forms.IntegerField(required=False)


IngredientFormSet = inlineformset_factory(
    Recette,
    RecetteIngredientUnit,
    form=IngredientForm,
    extra=0,          # 🔥 UN seul form vide
    can_delete=True  # 🔥 PAS de delete pour l’instant
)