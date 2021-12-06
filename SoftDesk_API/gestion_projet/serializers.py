from django.db import models
from django.db.models import fields
from rest_framework import serializers

from gestion_projet.models import Projects, Contributors, Issues


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author']


class InputProjectSerializer(serializers.ModelSerializer):
    class Meta:
       model = Projects
       fields = ['id', 'title', 'description', 'type']

class ProjectsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['permission', 'role']


class ContributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['user', 'project', 'permission', 'role']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'

class InputIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['title', 'description', 'tag', 'priority', 'status', 'assignee_user_id']
