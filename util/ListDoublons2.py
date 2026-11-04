from collections import defaultdict
from recettes.models import RecetteIngredientUnit
from recettes.models import RecetteIngredientUnit
from collections import defaultdict
import unicodedata
import re

doublons = defaultdict(list)

def normaliser(texte):
    texte = texte.strip().lower()
    texte = unicodedata.normalize('NFKD', texte)
    texte = ''.join(
        c for c in texte
        if not unicodedata.combining(c)
    )
    return re.sub(r'\s+', ' ', texte)


lignes = (
    RecetteIngredientUnit.objects
    .exclude(description__isnull=True)
    .exclude(description='')
    .select_related('recette')
    .order_by('recette__titre', 'ordre', 'id')
)

groupes = defaultdict(list)

for ligne in lignes:
    groupes[normaliser(ligne.description)].append(ligne)

for cle, items in sorted(groupes.items()):
    variantes = sorted({item.description for item in items})

    if len(variantes) > 1:
        print(f"\n{'=' * 70}")
        print(f"GROUPE : {cle}")
        print(f"VARIANTES : {variantes}")

        for item in items:
            print(
                f"ID={item.id} | "
                f"Recette={item.recette.titre} | "
                f"Qte={item.qte} | "
                f"Unité={item.unit} | "
                f"Description={item.description}"
            )