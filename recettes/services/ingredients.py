def generer_libelle_affichage(ingredient_unit):
    """
    Génère le libellé affiché d'un ingrédient de recette.
    """

    if ingredient_unit.unit == "--":
        return ingredient_unit.description or ""

    if not ingredient_unit.ingredient:
        return ingredient_unit.description or ""

    nom = ingredient_unit.ingredient.nom.strip()

    precision = (ingredient_unit.description or "").strip()

    return " ".join(
        partie
        for partie in [nom, precision]
        if partie
    )

def mettre_a_jour_libelle_affichage(ingredient_unit):
    libelle = generer_libelle_affichage(ingredient_unit)

    if ingredient_unit.libelle_affichage != libelle:
        ingredient_unit.libelle_affichage = libelle
        ingredient_unit.save(
            update_fields=["libelle_affichage"]
        )

def mettre_a_jour_libelles_ingredient(ingredient):
    for ingredient_unit in ingredient.recette_ingredients.all():
        mettre_a_jour_libelle_affichage(ingredient_unit)

def reconstruire_libelles_affichage():
    for ingredient_unit in RecetteIngredientUnit.objects.select_related(
        "ingredient"
    ).iterator():
        libelle = generer_libelle_affichage(ingredient_unit)

        if ingredient_unit.libelle_affichage != libelle:
            ingredient_unit.libelle_affichage = libelle
            ingredient_unit.save(
                update_fields=["libelle_affichage"]
            )
