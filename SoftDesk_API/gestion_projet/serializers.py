from rest_framework import serializers

from gestion_projet.models import Projects


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author']


class InputProjectSerializer(serializers.ModelSerializer):
    class Meta:
       model = Projects
       fields = ['id', 'title', 'description', 'type']
