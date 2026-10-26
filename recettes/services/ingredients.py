
from recettes.models import RecetteIngredientUnit


def generer_libelle_affichage(ingredient_unit):
    """
    Génère le libellé de l'ingrédient sans quantité ni unité.

    Les groupes d'ingrédients conservent leur titre.
    Les ingrédients sans référence conservent leur description
    historique, afin de préserver les données pendant la migration.
    """

    # Une ligne de groupe n'est pas un ingrédient.
    if ingredient_unit.unit == "--":
        return (ingredient_unit.description or "").strip()

    ingredient = ingredient_unit.ingredient

    # Compatibilité temporaire avec les anciennes lignes.
    if ingredient is None:
        return (ingredient_unit.description or "").strip()

    nom = ingredient.nom.strip()
    precision = (ingredient_unit.description or "").strip()

    # Le pluriel est explicite dans le référentiel.
    qte = ingredient_unit.qte
    if qte is not None and qte > 1 and ingredient.nom_pluriel:
        nom = ingredient.nom_pluriel.strip()

    return " ".join(partie for partie in (nom, precision) if partie)


def mettre_a_jour_libelle_affichage(ingredient_unit):
    """
    Recalcule et enregistre le libellé uniquement s'il a changé.
    """
    libelle = generer_libelle_affichage(ingredient_unit)

    if ingredient_unit.libelle_affichage != libelle:
        ingredient_unit.libelle_affichage = libelle
        ingredient_unit.save(update_fields=["libelle_affichage"])


def mettre_a_jour_libelles_ingredient(ingredient):
    """
    Recalcule les libellés de toutes les recettes utilisant
    cet ingrédient.
    """
    for ingredient_unit in ingredient.recette_ingredients.all():
        mettre_a_jour_libelle_affichage(ingredient_unit)


def reconstruire_libelles_affichage():
    """
    Recalcule les libellés de toutes les lignes d'ingrédients.
    À utiliser lors d'une reconstruction volontaire.
    """
    lignes = RecetteIngredientUnit.objects.select_related(
        "ingredient"
    )

    for ingredient_unit in lignes.iterator():
        mettre_a_jour_libelle_affichage(ingredient_unit)
