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

descriptions = (
    RecetteIngredientUnit.objects
    .exclude(description__isnull=True)
    .exclude(description='')
    .values_list('description', flat=True)
    .distinct()
)

for description in descriptions:
    doublons[normaliser(description)].append(description)

for cle, variantes in sorted(doublons.items()):
    if len(variantes) > 1:
        print(f"{cle} : {variantes}")