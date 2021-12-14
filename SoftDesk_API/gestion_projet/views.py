import re
from django.conf import settings
from django.http import Http404
from rest_framework import status
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions
# from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from gestion_projet.serializers import ContributorsSerializer


# from rest_framework.fields import CurrentUserDefault

from authentication.models import User
from authentication.serializers import UserSerializer
from gestion_projet.models import Projects, Contributors, Issues, Comments
from gestion_projet.serializers import ProjectSerializer, InputProjectSerializer, CreateContributorSerializer, IssueSerializer, InputIssueSerializer, CommentSerializer, InputCommentSerializer
from gestion_projet.permissions import IsOwnerOrReadOnly, IsOwnerOrContributor

# class ProjetViewset(ModelViewSet):

#     serializer_class = ProjetSerializer
#     permission_classes = [IsAuthenticated]


#     def get_queryset(self):
#         return Projets.objects.all()

#     def create(self, request, *args, **kwargs):
        # return super().create(request, *args, **kwargs)

class ProjectList(APIView):
    """
    List all projects, or create a new project.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        projects = Projects.objects.filter(author=request.user) | Projects.objects.filter(contributor=request.user)

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # TODO : ajouter une contribution
        serializer = InputProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author=request.user)
            project_serializer = ProjectSerializer(project)
            Contributors.objects.create(
                user = request.user,
                project = project,
                # TODO : change permissions
                permission = 'test',
                role = 'auhtor'
            )
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrContributor, IsOwnerOrReadOnly]

    def get_object(self, request, project_id):
        try:
            project = Projects.objects.get(pk=project_id)
            return project
        except Projects.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(request, pk)
        # TODO : add permissions du projet
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(request, pk)
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(request, pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response('Project Deleted', status=status.HTTP_200_OK)


class ContributorsList(APIView):
    """
    List all project's collaborators, or attach a new collaborator.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        users = User.objects.filter(contributions=pk)
        if users is None:
            print('Dommage...')
        else:
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        try:
            user = User.objects.get(email=request.POST.get('email'))
        except User.DoesNotExist:
            raise Http404
        serializer = CreateContributorSerializer(data=request.data)
        try:
            project = Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            raise Http404
        try:
            Contributors.objects.get(user=user, project=project)
            return Response("Error : contributor already added", status=status.HTTP_409_CONFLICT)
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
    # TODO : ajout permission isAuthor ?
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, project_id, user_id):
        try:
            contributor = Contributors.objects.get(user=user_id, project=project_id)
            projet = Projects.objects.get(id=project_id)
            self.check_object_permissions(request, projet)
            contributor.delete()
            return Response(_("user deleted of this project"))
        except Contributors.DoesNotExist:
            raise Http404


class IssuesList(APIView):
    """
    List all issues of a selected project, or create an issue.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        issues = Issues.objects.filter(project_id=pk)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = InputIssueSerializer(data=request.data)
        try:
            project = Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            raise Http404
        if serializer.is_valid():
            issue = serializer.save(author=request.user, project_id=project)
            issue_serializer = IssueSerializer(issue)
            return Response(issue_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(APIView):
    """
    Update an issue or delete it.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, project_id, issue_id):
        issue = Issues.objects.get(pk=issue_id)
        self.check_object_permissions(request, issue)
        serializer = InputIssueSerializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            issue = serializer.save(author_user_id=issue.author, project_id=issue.project_id)
            issue_serializer = IssueSerializer(issue)
            return Response(issue_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id):
        try:
            issue = Issues.objects.get(pk=issue_id, project_id=project_id)
            self.check_object_permissions(request, issue)
            issue.delete()
            return Response(_("issue deleted of this project"))
        except Issues.DoesNotExist:
            raise Http404


class CommentsList(APIView):
    """
    List Comments binded to an issue, or create a comment
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, issue_id):
        # TODO ; ajouter la verification du projet
        comment = Comments.objects.filter(issue_id=issue_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, project_id, issue_id):
        serializer = InputCommentSerializer(data=request.data)
        issue = Issues.objects.get(id=issue_id)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, issue_id=issue)
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """
    update / delete / get : comment with an id
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, project_id, issue_id, comment_id):
        # TODO : recuperer projet et issue
        comment = Comments.objects.get(id=comment_id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            comment = serializer.save()
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id, comment_id):
        try:
            comment = Comments.objects.get(id=comment_id)
            self.check_object_permissions(request, comment)
            comment.delete()
            return Response(_('comment deleted'))
        except Comments.DoesNotExist:
            raise Http404

    def get(self, request, project_id, issue_id, comment_id):
        try:
            comment = Comments.objects.get(id=comment_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comments.DoesNotExist:
            raise Http404
