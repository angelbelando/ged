from django.db import models
from django.contrib.auth.models import User
from datetime import date

DIR_PHOTOS = 'Photos/'

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class Recette(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='recettes')
    temps_preparation = models.IntegerField()
    temps_cuisson = models.IntegerField()
    nombre_couverts = models.IntegerField()
    ingredients = models.TextField(blank=True)
    etapes = models.TextField()
    conseils = models.TextField(default=None)
    image = models.ImageField(upload_to=DIR_PHOTOS, null=True, blank=True)
    video_url_youtube = models.URLField(max_length=200, unique=True, blank=True)
    note = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recettes', default=None, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre



# Modèle intermédiaire
class RecetteIngredientUnit(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='recette_ingredient_units')
    qte = models.DecimalField(decimal_places=2, max_digits=10)
    unit = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.recette.titre} - {self.description}"
