from django.db.models import Sum
from biens.models import Bien

resultats = Bien.objects.values('rubrique').annotate(total_montant=Sum('montant'))
for resultat in resultats:
    print(f"Rubrique: {resultat['rubrique']}, Total: {resultat['total_montant']}")
