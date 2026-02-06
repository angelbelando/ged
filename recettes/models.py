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
    conseils = models.TextField(default=None, blank=True, null=True)
    image = models.ImageField(upload_to=DIR_PHOTOS, null=True, blank=True)
    video_url_youtube = models.URLField(max_length=200, unique=False, blank=True, null=True)
    note = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recettes', default=None, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

UNITES = (
    ('--', 'Groupe Ingrédients'),
    ('  ', 'Ingrédient sans unité'),
    ('ail/s', 'Ail'),
    ('banane/s', 'Banane'),
    ('barre/s', 'Barre'),
    ('barre/s de chocolat', 'Barre de chocolat'),
    ('barres/s', 'Barres'),
    ('barquette/s', 'Barquette'),
    ('bocal/s', 'Bocal'),
    ('bol/s', 'Bol'),
    ('boîte/s', 'Boîte'),
    ('boîte/s de conserve', 'Boîte de conserve'),
    ('bouteille/s', 'Bouteille'),
    ('branche/s', 'Branche'),
    ('brin/s', 'Brin'),
    ('brique/s', 'Brique'),
    ('briques/s', 'Briques'),
    ('carotte/s', 'Carotte'),
    ('citron/s', 'Citron'),
    ('cl', 'Centilitres'),
    ('cuillère/s à café', 'Cuillère à café'),
    ('cuillère/s à soupe', 'Cuillère à soupe'),
    ('dl', 'Décilitres'),
    ('feuille/s', 'Feuille'),
    ('filet/s', 'Filet'),
    ('g', 'Grammes'),
    ('gousse/s', 'Gousse'),
    ('jaune/s', 'Jaune'),
    ('jus', 'Jus'),
    ('kg', 'Kilogrammes'),
    ('Lamelle/s', 'Lamelle'),
    ('l', 'Litres'),
    ('ml', 'Millilitres'),
    ('morceau/x', 'Morceau'),
    ('noix', 'Noix'),
    ('noisette/s', 'Noisettte'),
    ('oignon/s', 'Oignon'),
    ('oeuf/s', 'Oeuf'),
    ('orange/s', 'Orange'),
    ('paquet/s', 'Paquet'),
    ('pincée/s', 'Pincée'),
    ('pièce/s', 'Pièce'),
    ('poignée/s', 'Poignée'),
    ('poivre', 'Poivre'),
    ('pomme/s', 'Pomme'),
    ('pot/s', 'Pot'),
    ('pots/s', 'Pots'),
    ('rouleau/x', 'Rouleaux'),
    ('sachet', 'Sachet'),
    ('sachet/s', 'Sachet'),
    ('sel', 'Sel'),
    ('tasse/s', 'Tasse'),
    ('tomate/s', 'Tomate'),
    ('tour/s de moulin', 'Tour de moulin'),
    ('tranche/s', 'Tranche'),
    ('verre/s', 'Verre'),
    ('zeste/s', 'Zeste'),

)

class RecetteIngredientUnit(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='recette_ingredient_units')
    qte = models.DecimalField(decimal_places=2, max_digits=10,null=True)
    unit = models.CharField(choices=UNITES, max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    ordre = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.recette.titre} - {self.description}"
