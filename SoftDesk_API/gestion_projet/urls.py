from rest_framework import routers
from django.urls import path, include

from gestion_projet.views import ProjetViewset

router = routers.SimpleRouter()
router.register('projects', ProjetViewset, basename='projet')

urlpatterns = [
    path('', include(router.urls)),
]
