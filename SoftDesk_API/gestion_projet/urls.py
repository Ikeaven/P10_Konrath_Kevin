from rest_framework import routers
from django.urls import path, include

from gestion_projet import views

router = routers.DefaultRouter()
router.register('issues', views.IssueViewSet, basename='issue')

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:project_id>/', views.ProjectDetail.as_view()),
    path('projects/<int:project_id>/users/', views.ContributorsList.as_view()),
    path('projects/<int:project_id>/users/<int:user_id>/', views.DeleteContributor.as_view()),

    # path('projects/<int:project_id>/issues/', views.IssuesList.as_view()),
    # path('projects/<int:project_id>/issues/<int:issue_id>/', views.IssueDetail.as_view()),
    path('projects/<int:project_id>/', include(router.urls)),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', views.CommentsList.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/', views.CommentDetail.as_view()),

]
