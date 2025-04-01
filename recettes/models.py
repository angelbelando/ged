from django.db import models
from django.contrib.auth.models import User
from numpy import sum

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)  # Le nom de la catégorie doit être unique

    def __str__(self):
        return self.nom

# Modèle Recette existant
class Recette(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.ForeignKey(
        Categorie, on_delete=models.CASCADE, related_name='recettes'
    )  # Lien avec le modèle Categorie
    temps_preparation = models.IntegerField()
    temps_cuisson = models.IntegerField()
    ingredients = models.TextField()
    etapes = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    note_moyenne = models.FloatField(default=0.0)
    visites = models.PositiveIntegerField(default=0)

    def score_tendance(self):
        # Exemple de calcul de score : somme des visites et note moyenne pondérée
        return self.visites + (self.note_moyenne * 10)

    def __str__(self):
        return self.titre
    
    def update_note_moyenne(self):
        notes = Note.objects.filter(recette=self).values_list('valeur', flat=True)
        if notes:
            self.note_moyenne = round(sum(notes) / len(notes), 2)  # Arrondit à 2 décimales
        else:
            self.note_moyenne = 0.0  # Pas de notes, moyenne à 0
        self.save()

# Gestion des favoris
class Favori(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favoris'
    )  # L'utilisateur qui ajoute la recette aux favoris
    recette = models.ForeignKey(
        Recette, on_delete=models.CASCADE, related_name='favoris'
    )  # La recette ajoutée en favoris
    date_added = models.DateTimeField(auto_now_add=True)  # Date d'ajout aux favoris

    class Meta:
        unique_together = ('user', 'recette')  # Un utilisateur ne peut pas ajouter deux fois la même recette.

    def __str__(self):
        return f"{self.user.username} - {self.recette.titre}"
    

class Note(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='notes')
    valeur = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('utilisateur', 'recette')  # Empêche plusieurs notes par utilisateur pour une recette

    def __str__(self):
        return f"{self.valeur} étoile(s) par {self.utilisateur.username} pour {self.recette.titre}"
