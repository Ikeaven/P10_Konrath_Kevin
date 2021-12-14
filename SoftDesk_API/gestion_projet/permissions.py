from rest_framework import permissions
from gestion_projet.models import Projects

from gestion_projet.models import Contributors

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class IsOwnerOrContributor(permissions.BasePermission):
    """
    Object-level permission to only allow owners or contributors of a project
    """
    def has_object_permission(self, request, view, project):
        contributor = (Contributors.objects.filter(user=request.user) & Contributors.objects.filter(project=project))
        author = (Projects.objects.filter(author=request.user) & Projects.objects.filter(id=project.id))
        if contributor.exists() or author.exists():
            return True
        else:
            return False