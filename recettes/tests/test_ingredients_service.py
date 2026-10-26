
from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase

from recettes.services.ingredients import generer_libelle_affichage


from unittest.mock import patch

from django.test import TestCase

from recettes.models import (
    Categorie,
    Ingredient,
    Recette,
    RecetteIngredientUnit,
)
from recettes.services.ingredients import (
    mettre_a_jour_libelle_affichage,
)
class GenererLibelleAffichageTests(SimpleTestCase):

    def creer_ligne(
        self,
        *,
        nom="Tomate",
        nom_pluriel="Tomates",
        qte="1",
        unit="g",
        description="",
        libelle_affichage="",
    ):
        ingredient = SimpleNamespace(
            nom=nom,
            nom_pluriel=nom_pluriel,
        )

        return SimpleNamespace(
            ingredient=ingredient,
            qte=Decimal(qte) if qte is not None else None,
            unit=unit,
            description=description,
            libelle_affichage=libelle_affichage,
        )

    def test_ingredient_au_singulier(self):
        ligne = self.creer_ligne(qte="1")
        self.assertEqual(
            generer_libelle_affichage(ligne),
            "Tomate",
        )

    def test_ingredient_au_pluriel(self):
        ligne = self.creer_ligne(qte="3")
        self.assertEqual(
            generer_libelle_affichage(ligne),
            "Tomates",
        )

    def test_precision_conservee(self):
        ligne = self.creer_ligne(
            qte="3",
            description="mûres",
        )
        self.assertEqual(
            generer_libelle_affichage(ligne),
            "Tomates mûres",
        )

    def test_nom_sans_pluriel_reste_inchange(self):
        ligne = self.creer_ligne(
            nom="Farine",
            nom_pluriel="",
            qte="500",
            unit="g",
        )
        self.assertEqual(
            generer_libelle_affichage(ligne),
            "Farine",
        )

    def test_groupe_conserve_son_titre(self):
        ligne = self.creer_ligne(
            unit="--",
            description="Pour la béchamel",
        )
        self.assertEqual(
            generer_libelle_affichage(ligne),
            "Pour la béchamel",
        )

    def test_ligne_sans_ingredient(self):
        ligne = SimpleNamespace(
            ingredient=None,
            qte=Decimal("2"),
            unit="g",
            description="Ancienne description",
            libelle_affichage="",
        )
        self.assertEqual(
            generer_libelle_affichage(ligne),
            "Ancienne description",
        )

class MettreAJourLibelleAffichageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.categorie = Categorie.objects.create(
            nom="Tests ingrédients"
        )

        cls.recette = Recette.objects.create(
            titre="Recette de test",
            categorie=cls.categorie,
            temps_preparation=10,
            temps_cuisson=20,
            nombre_couverts=4,
            note=4,
        )

        cls.tomate = Ingredient.objects.create(
            nom="Tomate",
            nom_pluriel="Tomates",
        )

    def creer_ligne(self, **overrides):
        valeurs = {
            "recette": self.recette,
            "ingredient": self.tomate,
            "qte": Decimal("3"),
            "unit": "g",
            "description": "mûres",
            "libelle_affichage": "",
        }
        valeurs.update(overrides)

        return RecetteIngredientUnit.objects.create(**valeurs)

    def test_enregistre_le_libelle_calcule(self):
        ligne = self.creer_ligne()

        mettre_a_jour_libelle_affichage(ligne)

        ligne.refresh_from_db()

        self.assertEqual(
            ligne.libelle_affichage,
            "Tomates mûres",
        )

    def test_ne_sauvegarde_pas_si_le_libelle_est_deja_correct(self):
        ligne = self.creer_ligne(
            libelle_affichage="Tomates mûres"
        )

        with patch.object(
            ligne,
            "save",
            wraps=ligne.save,
        ) as sauvegarde:
            mettre_a_jour_libelle_affichage(ligne)

        sauvegarde.assert_not_called()

    def test_sauvegarde_si_le_libelle_est_different(self):
        ligne = self.creer_ligne(
            libelle_affichage="Ancien libellé"
        )

        with patch.object(
            ligne,
            "save",
            wraps=ligne.save,
        ) as sauvegarde:
            mettre_a_jour_libelle_affichage(ligne)

        sauvegarde.assert_called_once_with(
            update_fields=["libelle_affichage"]
        )

        ligne.refresh_from_db()

        self.assertEqual(
            ligne.libelle_affichage,
            "Tomates mûres",
        )

    def test_groupe_conserve_son_titre(self):
        ligne = self.creer_ligne(
            ingredient=None,
            unit="--",
            description="Pour la béchamel",
        )

        mettre_a_jour_libelle_affichage(ligne)

        ligne.refresh_from_db()

        self.assertEqual(
            ligne.libelle_affichage,
            "Pour la béchamel",
        )
