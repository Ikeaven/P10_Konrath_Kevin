from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from gestion_projet.models import Projets
from gestion_projet.serializers import ProjetSerializer


class ProjetViewset(ModelViewSet):

    serializer_class = ProjetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Projets.objects.all()
