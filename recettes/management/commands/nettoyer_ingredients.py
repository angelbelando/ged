from django.core.management.base import BaseCommand
from django.db import transaction

from recettes.models import RecetteIngredientUnit


# Correspondances exactes :
# ancienne description -> description corrigée
#
# Seules les descriptions sont modifiées.
# Aucune ligne n'est supprimée ou fusionnée.

CORRECTIONS = {
    # Beurre
    "beurre": "Beurre",

    # Bouquet garni
    "bouquet garni": "Bouquet garni",

    # Courgette
    "courgette": "Courgette",

    # Câpres
    "de capres": "de câpres",

    # Champignons
    "de Champignons de Paris": "de champignons de Paris",

    # Cognac
    "de cognac": "de Cognac",

    # Crème fraîche
    "de crème fraiche": "de crème fraîche",

    # Farine
    "De farine": "de farine",
    'de Farine Francine "Ma brioche Maison"':
        'de farine Francine "Ma brioche maison"',

    # Feta
    "de Feta": "de feta",

    # Laurier
    "de Laurier": "de laurier",

    # Moutarde
    "de moutarde de Dijon": "de moutarde de Dijon",

    # Parmesan
    "de Parmesan": "de parmesan",
    "de parmesan rapé": "de parmesan râpé",
    "de Parmesan râpé": "de parmesan râpé",

    # Piment d'Espelette
    "de Piment d'Espelette": "de piment d'Espelette",
    "de piment d'Espelette": "de piment d'Espelette",
    "de piment d'espelette": "de piment d'Espelette",
    "Piment d'espelette": "Piment d'Espelette",
    "piment d'Espelette": "Piment d'Espelette",

    # Quinoa
    "de Quinoa": "de quinoa",

    # Rhum
    "de Rhum": "de rhum",
    "de Rhum brun": "de rhum brun",

    # Safran
    "de safran": "de Safran",

    # Sauce soja
    "De sauce soja salé": "de sauce soja salé",

    # Sel et thym
    "De sel": "de sel",
    "de Thym": "de thym",

    # Eau
    "D’eau": "d’eau",
    "Eau": "Eau",

    # Échalotes
    "Echalotes": "Échalotes",
    "échalotes": "Échalotes",
    "échalotte": "Échalote",
    "Echalotte": "Échalote",
    "echalotte": "Échalote",

    # Entier / entiers
    "Entier": "entier",
    "Entiers": "entiers",

    # Farine
    "farine": "Farine",

    # Gros oignon
    "gros oignon": "Gros oignon",

    # Huile d'olive
    "huile d'olive": "Huile d'olive",

    # Jus de citron
    "le jus d'un citron": "Le jus d'un citron",

    # Merguez
    "merguez": "Merguez",

    # Mozzarella
    "Mozzarella rapée": "de Mozzarella râpée",

    # Oignons
    "oignons": "Oignons",

    # Pâte à pizza
    "Pate à pizza": "Pâte à pizza",

    # Poivre
    "poivre": "Poivre",
    "poivre du moulin": "Poivre du moulin",
    "Poivre noir": "Poivre noir",
    "poivre noir": "Poivre noir",

    # Poivrons
    "poivron jaune": "Poivron jaune",
    "poivron rouge": "Poivron rouge",
    "Poivrons rouges": "Poivrons rouges",
    "poivrons rouges": "Poivrons rouges",

    # Quelques feuilles de basilic ou de persil
    "quelques feuilles de basilic ou de persil":
        "Quelques feuilles de basilic ou de persil",

    # Sauce tomate
    "Sauce Tomate": "Sauce tomate",

    # Sel
    "sel": "Sel",
    "Sel et poivre": "Sel et poivre",
    "Sel et  poivre": "Sel et poivre",
    "Sel et Poivre": "Sel et poivre",
    "Sel et poivre du moulin": "Sel et poivre du moulin",
    "Sel et poivre noir du moulin": "Sel et poivre noir du moulin",

    # Sucre glace
    "sucre glace": "Sucre glace",
}


class Command(BaseCommand):
    help = "Corrige les descriptions des ingrédients sans supprimer ni fusionner de lignes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Applique réellement les corrections.",
        )

    def handle(self, *args, **options):
        appliquer = options["apply"]

        self.stdout.write(
            self.style.WARNING(
                "\nMODE APPLICATION" if appliquer
                else "\nMODE SIMULATION — aucune modification"
            )
        )

        lignes = (
            RecetteIngredientUnit.objects
            .filter(description__in=CORRECTIONS.keys())
            .select_related("recette")
            .order_by("id")
        )

        modifications = []

        for ligne in lignes:
            ancienne = ligne.description
            nouvelle = CORRECTIONS[ancienne]

            # Ne rien faire si le libellé est déjà identique.
            if ancienne == nouvelle:
                continue

            modifications.append((ligne, ancienne, nouvelle))

        if not modifications:
            self.stdout.write(
                self.style.SUCCESS("Aucune correction à effectuer.")
            )
            return

        self.stdout.write(
            f"\n{len(modifications)} ligne(s) à corriger :\n"
        )

        for ligne, ancienne, nouvelle in modifications:
            self.stdout.write(
                f"ID {ligne.pk} | {ligne.recette.titre}\n"
                f"  Avant : {ancienne}\n"
                f"  Après : {nouvelle}\n"
            )

        if not appliquer:
            self.stdout.write(
                self.style.WARNING(
                    "\nSimulation terminée. "
                    "Aucune donnée n'a été modifiée."
                )
            )
            self.stdout.write(
                "Pour appliquer ces corrections : "
                "python manage.py nettoyer_ingredients --apply"
            )
            return

        nombre_modifie = 0

        with transaction.atomic():
            for ligne, ancienne, nouvelle in modifications:
                resultat = (
                    RecetteIngredientUnit.objects
                    .filter(pk=ligne.pk, description=ancienne)
                    .update(description=nouvelle)
                )

                nombre_modifie += resultat

        self.stdout.write(
            self.style.SUCCESS(
                f"\n{nombre_modifie} description(s) corrigée(s)."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Aucune ligne supprimée ou fusionnée."
            )
        )
