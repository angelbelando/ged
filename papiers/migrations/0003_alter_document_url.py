# Generated by Django 5.1.4 on 2025-04-01 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papiers', '0002_alter_typedocument_precision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='url',
            field=models.URLField(blank=True, verbose_name='Lien vers document sur le Cloud'),
        ),
    ]
