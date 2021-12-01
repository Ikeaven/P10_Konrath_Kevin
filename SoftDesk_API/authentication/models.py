from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import BaseUserManager

from authentication.managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
