from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recette
from .utils.utils_api import build_recette_payload
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

class RecettesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    def get(self, request):

        recettes = Recette.objects.prefetch_related(
            "recette_ingredient_units"
        ).all()

        couverts = request.GET.get("couverts")

        if couverts:
            couverts = int(couverts)

        data = [
            build_recette_payload(recette, request, couverts)
            for recette in recettes
        ]

        return Response(data)

class RecetteDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):

        recette = Recette.objects.prefetch_related(
            "recette_ingredient_units"
        ).get(pk=pk)

        couverts = request.GET.get("couverts")

        if couverts:
            couverts = int(couverts)

        data = build_recette_payload(recette, request, couverts)

        return Response(data)
