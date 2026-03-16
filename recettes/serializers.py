from rest_framework import serializers
from .models import Recette


class IngredientSerializer(serializers.Serializer):
    quantite = serializers.CharField()
    unite = serializers.CharField()
    description = serializers.CharField()
    unite_display = serializers.CharField()


class EtapeSerializer(serializers.Serializer):
    texte = serializers.CharField()
    important = serializers.BooleanField()

class RecetteSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    titre = serializers.CharField()
    nombre_couverts = serializers.IntegerField()

    image = serializers.CharField(allow_null=True)
    video_url_youtube = serializers.URLField(allow_null=True)

    ingredients = IngredientSerializer(many=True)
    etapes = EtapeSerializer(many=True)
    conseils = EtapeSerializer(many=True)