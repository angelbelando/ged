# Generated by Django 5.1.4 on 2025-01-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_alter_document_mois'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='mois',
            field=models.IntegerField(choices=[(1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')], default='1', max_length=9, verbose_name='mois'),
        ),
    ]
