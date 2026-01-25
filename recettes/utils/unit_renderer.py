import re
# Nettoyer les unités en fonction de la quantité
def nettoyer_unite(texte, qte):
    remplacements = {
        '/s': 's' if qte > 1 else '',
        '/x': 'x' if qte > 1 else ''
    }
    for suffixe, remplacement in remplacements.items():
        texte = re.sub(rf'\b{re.escape(suffixe)}\b', remplacement, texte)
    return texte

def formatter_qte(qte):
    if qte == 0:
        return ""
    elif qte == int(qte):
        return str(int(qte))
    else:
        return str(round(qte, 1))


# Liste des recettes de nous
# modification

def convertir_unite(qte, unite):
    """Convertit automatiquement certaines unités vers une unité supérieure."""
    unite_base = unite.strip().lower()

    if unite_base in ["g", "gramme", "grammes"] and qte >= 1000:
        return qte / 1000, "kg"
    elif unite_base in ["ml", "millilitre", "millilitres"] and qte >= 1000:
        return qte / 1000, "L"
    elif unite_base in ["cl", "centilitre", "centilitres"] and qte >= 100:
        return qte / 100, "L"
    else:
        return qte, unite
