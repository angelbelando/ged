from .unit_renderer import nettoyer_unite, formatter_qte, convertir_unite


def build_recette_payload(recette, nombre_couverts=None):
    nb_ref = int(recette.nombre_couverts or 1)
    nb_couv = int(nombre_couverts) if nombre_couverts is not None else nb_ref

    ingredients = []
    for ing in recette.recette_ingredient_units.all().order_by("ordre", "id"):
        qte_base = float(ing.qte or 0)
        qte = qte_base / nb_ref * nb_couv

        qte, unite = convertir_unite(qte, ing.unit)
        qte_fmt = formatter_qte(qte)
        unite_fmt = nettoyer_unite(unite, qte)

        ingredients.append({
            "texte": f"{qte_fmt} {unite_fmt} {ing.description}",
        })

    etapes = []
    if recette.etapes:
        for ligne in recette.etapes.splitlines():
            txt = ligne.strip()
            if not txt:
                continue
            etapes.append({
                "type": "titre" if txt.startswith("-") else "item",
                "texte": txt[1:].strip() if txt.startswith("-") else txt
            })
    conseils = []
    if recette.conseils:
        for ligne_conseils in recette.conseils.splitlines():
            txt = ligne_conseils.strip()
            if not txt:
                continue
            conseils.append({
                "type": "titre" if txt.startswith("-") else "item",
                "texte": txt[1:].strip() if txt.startswith("-") else txt
            })
    return {
        "titre": recette.titre,
        "description": recette.description or "",
        "categorie": recette.categorie.nom if recette.categorie else "Non spécifiée",
        "nb_couverts": nb_couv,
        "temps_preparation": recette.temps_preparation or 0,
        "temps_cuisson": recette.temps_cuisson or 0,
        "image": recette.image.path if recette.image else None,
        "ingredients": ingredients,
        "etapes": etapes,
        "conseils": conseils,
        "note": int(recette.note or 0),
    }
