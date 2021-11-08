from django.http import response
from rest_framework.viewsets import ModelViewSet

from gestion_projet.models import Projets
from gestion_projet.serializers import ProjetSerializer

class ProjetViewset(ModelViewSet):

    serializer_class = ProjetSerializer

    def get_queryset(self):
        return Projets.objects.all()
