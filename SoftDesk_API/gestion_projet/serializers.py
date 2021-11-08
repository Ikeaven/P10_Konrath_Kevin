from django.db.models import fields
from rest_framework import serializers

from gestion_projet.models import Projets

class ProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projets
        fields = ['id', 'title', 'description', 'type', 'author']
