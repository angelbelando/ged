# Generated by Django 5.1.4 on 2025-03-25 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papiers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typedocument',
            name='precision',
            field=models.TextField(blank=True, verbose_name='précisions'),
        ),
    ]
