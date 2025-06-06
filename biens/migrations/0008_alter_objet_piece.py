# Generated by Django 5.1.4 on 2025-03-19 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0007_alter_objet_estimation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objet',
            name='piece',
            field=models.CharField(choices=[('Salon', 'Salon'), ('Salle à manger', 'Salle à manger'), ('Cuisine', 'Cuisine'), ('Terrasse SO', 'Terrasse SO'), ('Terrasse NE', 'Terrasse NE'), ('Chambre_Jérémy', 'Chambre Jérémy'), ('Chambre_Parents', 'Chambre Parents'), ('Bureau', 'Bureau'), ('Garage', 'Garage'), ('Devant Entrée', 'Devant Entrée'), ('Couloirs', 'Couloirs'), ('Salle de Bain', 'Salle de Bain'), ('Toilettes', 'Toilettes-WC'), ('Autre', 'Autre')], default='Autre', max_length=20, verbose_name='pièce'),
        ),
    ]
