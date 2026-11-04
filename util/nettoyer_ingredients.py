from django.core.management.base import BaseCommand
from recettes.models import RecetteIngredientUnit


class Command(BaseCommand):
    help = "Nettoyage des descriptions des ingrédients"

    def handle(self, *args, **options):

        lignes = RecetteIngredientUnit.objects.all()

        for ligne in lignes:
            self.stdout.write(
                f"{ligne.id} - {ligne.description}"
            )

        self.stdout.write(
            self.style.SUCCESS("Analyse terminée.")
        )