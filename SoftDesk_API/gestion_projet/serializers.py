# from django.db import models
# from django.db.models import fields
from rest_framework import serializers

from gestion_projet.models import Projects, Contributors, Issues, Comments


class ProjectSerializer(serializers.ModelSerializer):
    contributor = serializers.StringRelatedField(many=True)
    author = serializers.ReadOnlyField(source="author.email")

    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type", "author", "contributor"]


class InputProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type"]


class ContributorsSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()

    class Meta:
        model = Contributors
        fields = ["id", "user", "project", "permission", "role"]


class CreateContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ["permission", "role"]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"


class InputIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = [
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "assignee_user_id",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class InputCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["description"]
