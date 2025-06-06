# Generated by Django 5.2 on 2025-05-14 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recettes', '0010_alter_recetteingredientunit_qte'),
    ]

    operations = [
        migrations.AddField(
            model_name='recetteingredientunit',
            name='ordre',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='recetteingredientunit',
            name='unit',
            field=models.CharField(choices=[('g', 'Grammes'), ('kg', 'Kilogrammes'), ('l', 'Litres'), ('cl', 'Centilitres'), ('ml', 'Millilitres'), ('dl', 'Décilitres'), ('sel', 'Sel'), ('poivre', 'Poivre'), ('pièce/s', 'Pièce'), ('feuille/s', 'Feuille'), ('branche/s', 'Branche'), ('tranche/s', 'Tranche'), ('citron/s', 'Citron'), ('gousse/s', 'Gousse'), ('pomme/s', 'Pomme'), ('orange/s', 'Orange'), ('banane/s', 'Banane'), ('carotte/s', 'Carotte'), ('tomate/s', 'Tomate'), ('oignon/s', 'Oignon'), ('oeuf,s', 'Oeuf'), ('jaune/s', 'Jaune'), ('blanc/s', 'Blanc'), ('ail/s', 'Ail'), ('bouteille/s', 'Bouteille'), ('cuillère/s à café', 'Cuillère à café'), ('cuillère/s à soupe', 'Cuillère à soupe'), ('pincée/s', 'Pincée'), ('tour/s de moulin', 'Tour de moulin'), ('morceau/x', 'Morceau'), ('poignée/s', 'Poignée'), ('sachet/s', 'Sachet'), ('rouleaux/s', 'Rouleaux'), ('barre/s', 'Barre'), ('barre/s de chocolat', 'Barre de chocolat'), ('barre/s', 'Barre'), ('barres/s', 'Barres'), ('pot/s', 'Pot'), ('pots/s', 'Pots'), ('boîte/s de conserve', 'Boîte de conserve'), ('brique/s', 'Brique'), ('briques/s', 'Briques'), ('sachet', 'Sachet'), ('boîte/s', 'Boîte'), ('paquet/s', 'Paquet'), ('tasse/s', 'Tasse'), ('verre/s', 'Verre'), ('barquette/s', 'Barquette'), ('bocal/s', 'Bocal'), ('brin/s', 'Brin'), ('--', 'Paragraphe')], max_length=200),
        ),
    ]
