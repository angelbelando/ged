from .unit_renderer import formatter_qte, nettoyer_unite

def build_recette_payload(recette, request=None, nombre_couverts=None):

    if nombre_couverts is None:
        nombre_couverts = recette.nombre_couverts
    image_url = None

    if recette.image:
        if request:
            image_url = request.build_absolute_uri(recette.image.url)
        else:
            image_url = recette.image.url

    ingredients = [
        {
            "quantite": formatter_qte(
                round(ing.qte / recette.nombre_couverts * nombre_couverts, 1)
            ),
            "unite": ing.unit,
            "description": ing.description,
            "unite_display": nettoyer_unite(
                ing.unit,
                round(ing.qte / recette.nombre_couverts * nombre_couverts, 1)
            ),
        }
        for ing in recette.recette_ingredient_units.all().order_by("ordre", "id")
    ]

    etapes = [
        {"texte": e[1:].strip(), "important": True}
        if e.strip().startswith("-")
        else {"texte": e.strip(), "important": False}
        for e in recette.etapes.splitlines()
    ]

    conseils = [
        {"texte": c[1:].strip(), "important": True}
        if c.strip().startswith("-")
        else {"texte": c.strip(), "important": False}
        for c in recette.conseils.splitlines()
    ]

    return {
        "id": recette.id,
        "titre": recette.titre,
        "nombre_couverts": nombre_couverts,
        "image": image_url,
        "video_url_youtube": recette.video_url_youtube,
        "ingredients": ingredients,
        "etapes": etapes,
        "conseils": conseils,
    }