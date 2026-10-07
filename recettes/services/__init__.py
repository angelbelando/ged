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