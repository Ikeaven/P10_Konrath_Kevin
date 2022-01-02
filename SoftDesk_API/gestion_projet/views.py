from django.conf import settings
from django.http import Http404
from rest_framework import status
from django.utils.translation import ugettext_lazy as _

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets


from gestion_projet.serializers import ContributorsSerializer
from authentication.models import User
from authentication.serializers import UserSerializer
from gestion_projet.models import Projects, Contributors, Issues, Comments
from gestion_projet.serializers import ProjectSerializer, CreateContributorSerializer, IssueSerializer, InputIssueSerializer, CommentSerializer, InputCommentSerializer
from gestion_projet.permissions import IsOwnerOrReadOnly, IsProjectOwnerOrContributor, IsIssueAuthor, IsCommentAuthor


##############################
# PROJECT LIST WITH API WIEW #
##############################

# class ProjectList(APIView):
#     """
#     List all projects, or create a new project.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         projects = Projects.objects.filter(author=request.user) | Projects.objects.filter(contributor=request.user)

#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = InputProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             project = serializer.save(author=request.user)
#             project_serializer = ProjectSerializer(project)
#             Contributors.objects.create(
#                 user = request.user,
#                 project = project,
#                 # TODO : change permissions
#                 permission = "author",
#                 role = 'auhtor'
#             )
#             return Response(project_serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------

##############################
# PROJECT LIST WITH GENERICS #
##############################

class ProjectList(generics.ListCreateAPIView):
    """
    List all project, or create a new project
    """

    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrContributor]

    def get_queryset(self):
        user = self.request.user
        return user.contributions.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributors.objects.create(
                user = self.request.user,
                project = project,
                permission = "author",
                role = 'auhtor'
            )

# ------------------------------------------------------------------------------------

#################################
#  Project detail with APIView  #
#################################

# class ProjectDetail(APIView):
#     """
#     Retrieve, update or delete a project instance.
#     """
#     permission_classes = [IsAuthenticated, IsOwnerOrContributor, IsOwnerOrReadOnly]

#     def get_object(self, request, project_id):
#         try:
#             project = Projects.objects.get(pk=project_id)
#             return project
#         except Projects.DoesNotExist:
#             return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, project_id, format=None):
#         project = self.get_object(request, project_id)
#         self.check_object_permissions(request, project)
#         serializer = ProjectSerializer(project)
#         return Response(serializer.data)

#     def put(self, request, project_id, format=None):
#         project = self.get_object(request, project_id)
#         self.check_object_permissions(request, project)
#         serializer = ProjectSerializer(project, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, project_id, format=None):
#         project = self.get_object(request, project_id)
#         self.check_object_permissions(request, project)
#         project.delete()
#         return Response({"detail":'Project Deleted'}, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------

#################################
#  Project detail with generics #
#################################

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a project instance.
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    lookup_url_kwarg = 'project_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsProjectOwnerOrContributor]

# ------------------------------------------------------------------------------------


##################################
#  Contributor list with APIView #
##################################
class ContributorsList(APIView):
    """
    List all project's collaborators, or attach a new collaborator.
    """
    permission_classes = [IsAuthenticated, IsProjectOwnerOrContributor]

    def get(self, request, project_id, format=None):
        users = User.objects.filter(contributions=project_id)
        project = Projects.objects.get(id=project_id)
        self.check_object_permissions(request, project)
        if users.exists():
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail":"No Collaborator for this project"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, project_id, format=None):
        try:
            user = User.objects.get(email=request.POST.get('collaborator'))
        except User.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CreateContributorSerializer(data=request.data)
        try:
            project = Projects.objects.get(pk=project_id)
            self.check_object_permissions(request, project)
        except Projects.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            Contributors.objects.get(user=user, project=project)
            return Response({"detail":"contributor already added"}, status=status.HTTP_409_CONFLICT)
        except Contributors.DoesNotExist:

            if serializer.is_valid():
                serializer.save(project=project, user=user)
                contributor = Contributors.objects.get(project=project, user=user)
                contributor_serializer = ContributorsSerializer(contributor)
                return Response(contributor_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteContributor(APIView):
    """
    Delete a contributor of the selected project.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, project_id, user_id):

        try:
            contributor = Contributors.objects.get(user=user_id, project=project_id)
            projet = Projects.objects.get(id=project_id)
            self.check_object_permissions(request, projet)
            if contributor.user == projet.author:
                return Response(({"detail":"Author cannot be deleted"}), status=status.HTTP_403_FORBIDDEN)
            else:
                contributor.delete()
                return Response(({"detail":"user deleted of this project"}))
        except Contributors.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)


#########################################################
#  Issues list - create - update - delete with APIView  #
#########################################################

# class IssuesList(APIView):
#     """
#     List all issues of a selected project, or create an issue.
#     """

#     permission_classes = [IsAuthenticated, IsOwnerOrContributor]

#     def get(self, request, project_id, format=None):
#         project = Projects.objects.get(id=project_id)
#         self.check_object_permissions(request, project)
#         issues = Issues.objects.filter(project_id=project_id)
#         serializer = IssueSerializer(issues, many=True)
#         return Response(serializer.data)

#     def post(self, request, project_id, format=None):
#         serializer = InputIssueSerializer(data=request.data)
#         try:
#             project = Projects.objects.get(pk=project_id)
#             self.check_object_permissions(request, project)
#         except Projects.DoesNotExist:
#             return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
#         if serializer.is_valid():
#             issue = serializer.save(author=request.user, project_id=project)
#             issue_serializer = IssueSerializer(issue)
#             return Response(issue_serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class IssueDetail(APIView):
#     """
#     Update an issue or delete it.
#     """
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

#     def put(self, request, project_id, issue_id):
#         issue = Issues.objects.get(pk=issue_id)
#         self.check_object_permissions(request, issue)
#         serializer = InputIssueSerializer(issue, data=request.data, partial=True)
#         if serializer.is_valid():
#             issue = serializer.save(author_user_id=issue.author, project_id=issue.project_id)
#             issue_serializer = IssueSerializer(issue)
#             return Response(issue_serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, project_id, issue_id):
#         try:
#             issue = Issues.objects.get(pk=issue_id, project_id=project_id)
#             self.check_object_permissions(request, issue)
#             issue.delete()
#             return Response({"detail":"issue deleted of this project"})
#         except Issues.DoesNotExist:
#             return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

# ------------------------------------------------------------------------------------


##############################################################
#  Issues list - create - update - delete with ModelViewSet  #
##############################################################


class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = generics.get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

class IssueViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer
    lookup_fields = ('project_id', 'pk')

    def get_permissions(self):
        if self.action in ('update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsIssueAuthor]
        elif self.action in ('list', 'create'):
            self.permission_classes = [IsAuthenticated, IsProjectOwnerOrContributor]
        else:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return super(self.__class__, self).get_permissions()

    def list(self, request, project_id):
        project = Projects.objects.get(pk=project_id)
        self.check_object_permissions(request, project)
        queryset = Issues.objects.filter(project_id=project_id)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_id, *args, **kwargs):
        serializer = InputIssueSerializer(data=request.data)
        try:
            project = Projects.objects.get(pk=project_id)
            self.check_object_permissions(request, project)
        except Projects.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            issue = serializer.save(author=request.user, project_id=project)
            issue_serializer = IssueSerializer(issue)
            return Response(issue_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, project_id, pk, *args, **kwargs):
        project = Projects.objects.get(pk=project_id)
        issue = Issues.objects.get(pk=pk)
        self.check_object_permissions(request, [issue, project])
        serializer = InputIssueSerializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            issue = serializer.save(author_user_id=issue.author, project_id=issue.project_id)
            issue_serializer = IssueSerializer(issue)
            return Response(issue_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_id, pk):
        try:
            project = Projects.objects.get(pk=project_id)
            issue = Issues.objects.get(pk=pk)
            self.check_object_permissions(request, [issue, project])
            issue.delete()
            return Response({"detail":"issue deleted of this project"})
        except Issues.DoesNotExist:
            print('YOUPLABOUM')
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

# ------------------------------------------------------------------------------------


########################################
#  Comment list - create with APIview  #
########################################
class CommentsList(APIView):
    """
    List Comments binded to an issue, or create a comment
    """

    permission_classes = [IsAuthenticated, IsProjectOwnerOrContributor]

    def get(self, request, project_id, issue_id):
        # TODO ; ajouter la verification du projet
        project = Projects.objects.get(id=project_id)

        self.check_object_permissions(request, project)
        comment = Comments.objects.filter(issue_id=issue_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, project_id, issue_id):
        project = Projects.objects.get(id=project_id)
        self.check_object_permissions(request, project)
        serializer = InputCommentSerializer(data=request.data)
        issue = Issues.objects.get(id=issue_id)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, issue_id=issue)
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##################################################
#  Comment update - delete - get : with APIview  #
##################################################

class CommentDetail(APIView):
    """
    update / delete / get : comment with an id
    """
    # TODO : IsCommentOwner
    permission_classes = [IsAuthenticated, IsCommentAuthor]


    def put(self, request, project_id, issue_id, comment_id):
        comment = Comments.objects.get(id=comment_id)
        project = Projects.objects.get(id=project_id)
        self.check_object_permissions(request, [comment, project])
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            comment = serializer.save()
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id, comment_id):
        try:
            comment = Comments.objects.get(id=comment_id)
            project = Projects.objects.get(id=project_id)
            self.check_object_permissions(request, [comment, project])
            comment.delete()
            return Response({"detail":'comment deleted'})
        except Comments.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, project_id, issue_id, comment_id):
        # Check if user is contributor or author
        contributor = Contributors.objects.filter(user=request.user) & Contributors.objects.filter(project_id=project_id)
        author = (Projects.objects.filter(author=request.user) & Projects.objects.filter(id=project_id))
        if contributor.exists() or author.exists():
            try:
                # Check if comment_id correspond to issue_id
                if project_id == Issues.objects.get(id=issue_id).project_id.id:
                    # Check if issue_id correspond to comment_id
                    if issue_id == Comments.objects.get(id=comment_id).issue_id.id:
                        comment = Comments.objects.get(id=comment_id)
                        serializer = CommentSerializer(comment)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({"detail": "Comment not attach to this issue."}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"detail": "Issue not in project."}, status=status.HTTP_403_FORBIDDEN)
            except Issues.DoesNotExist:
                return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
            except Comments.DoesNotExist:
                return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)