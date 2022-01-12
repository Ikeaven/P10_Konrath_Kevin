from rest_framework import permissions

# from SoftDesk_API.gestion_projet.models import Projects
from gestion_projet.models import Issues, Contributors, Comments


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        contributor = Contributors.objects.get(user=request.user, project=obj)
        print(contributor.permission)
        return contributor.permission == "author"


# class IsProjectOwnerOrContributor(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners for update or contributors of a project
#     """
#     def has_object_permission(self, request, view, project):
#         if request.method == 'GET':
#               contributor = (
#                   Contributors.objects.filter(user=request.user) & Contributors.objects.filter(project=project)
#               )
#             author = (Projects.objects.filter(author=request.user) & Projects.objects.filter(id=project.id))
#             if contributor.exists() or author.exists():
#                 return True
#             else:
#                 return False
#         elif request.method in ('PUT', 'DELETE', 'PATCH', 'POST'):
#             # TODO : LIGNE DU DESSOUS A VERIFIER ...
#             author = (Projects.objects.filter(author=request.user) & Projects.objects.filter(id=project.id))
#             if author.exists():
#                 return True
#             else:
#                 return False
#         else:
#             return False


class IsProjectOwnerOrContributor(permissions.BasePermission):
    """
    Object-level permission to only allow owners for update or contributors of a project
    """

    def has_object_permission(self, request, view, project):
        contributor = Contributors.objects.filter(
            project=project
        ) & Contributors.objects.filter(user=request.user)
        if contributor.exists():
            return True
        else:
            return False


class IsIssueAuthor(permissions.BasePermission):
    """
    Object-level permission to only allow owners of issue to update/delete it.
    """

    message = "Access denied, you don't have permissions to do this"

    def has_object_permission(self, request, view, obj):
        """
        Check permission for issues
        obj is a list => [issue, project]
        """
        contributor = Contributors.objects.filter(
            project=obj[1]
        ) & Contributors.objects.filter(user=request.user)
        if contributor.exists():
            if obj[0] in Issues.objects.filter(author=request.user):
                return True
            else:
                return False
        else:
            return False


class IsCommentAuthor(permissions.BasePermission):
    """
    Object-level permission to only allow owners of comment to update/delete it.
    """

    message = "Access denied, you don't have permissions to do this"

    def has_object_permission(self, request, view, obj):
        """
        Check permission for comment
        obj is a list => [comment, project]
        """
        contributor = Contributors.objects.filter(
            project=obj[1]
        ) & Contributors.objects.filter(user=request.user)
        if contributor.exists():
            if obj[0] in Comments.objects.filter(author=request.user):
                return True
            else:
                return False
        else:
            return False
