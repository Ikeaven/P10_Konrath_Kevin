from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']