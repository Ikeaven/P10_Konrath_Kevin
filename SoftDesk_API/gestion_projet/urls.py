from rest_framework import routers
from django.urls import path, include

from gestion_projet import views

# router = routers.SimpleRouter()
# router.register('projects', ProjetViewset, basename='projects')

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view())
    # path('', include(router.urls)),
]
