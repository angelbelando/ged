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
('g', 'Grammes'),
('kg', 'Kilogrammes'),  
('l', 'Litres'),
('cl', 'Centilitres'),
('ml', 'Millilitres'),
('dl', 'Décilitres'),
('sel', 'Sel'),
('poivre', 'Poivre'),
('pièce/s', 'Pièce'),
('feuille/s', 'Feuille'),
('branche/s', 'Branche'),
('tranche/s', 'Tranche'),
('citron/s', 'Citron'),
('gousse/s', 'Gousse'),
('pomme/s', 'Pomme'),
('orange/s', 'Orange'),
('banane/s', 'Banane'),
('carotte/s', 'Carotte'),
('tomate/s', 'Tomate'),
('oignon/s', 'Oignon'),
('oeuf,s', 'Oeuf'),
('jaune/s', 'Jaune'),
('blanc/s', 'Blanc'),
('ail/s', 'Ail'),
('bouteille/s', 'Bouteille'),
('cuillère/s à café', 'Cuillère à café'),
('cuillère/s à soupe', 'Cuillère à soupe'),
('pincée/s', 'Pincée'),
('tour/s de moulin', 'Tour de moulin'),
('morceau/x', 'Morceau'),
('poignée/s', 'Poignée'),
('sachet/s', 'Sachet'),
('sachets/s', 'Sachets'),
('barre/s', 'Barre'),
('barres/s', 'Barres'),
('pot/s', 'Pot'),
('pots/s', 'Pots'),
('boîte/s de conserve', 'Boîte de conserve'),
('brique/s', 'Brique'),
('briques/s', 'Briques'),
('sachet', 'Sachet'),
('boîte/s', 'Boîte'),
('paquet/s', 'Paquet'),
('tasse/s', 'Tasse'), 
('verre/s', 'Verre'),
('barquette/s', 'Barquette'),
('bocal/s', 'Bocal'),
('brin/s', 'Brin'),
('--', 'Paragraphe'),
)
class RecetteIngredientUnit(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='recette_ingredient_units')
    qte = models.DecimalField(decimal_places=2, max_digits=10,null=True)
    unit = models.CharField(choices=UNITES, max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.recette.titre} - {self.description}"
