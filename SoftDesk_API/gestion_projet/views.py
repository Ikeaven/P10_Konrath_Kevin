import re
from django.conf import settings
from django.http import Http404
from rest_framework import status
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
# from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView


# from rest_framework.fields import CurrentUserDefault

from authentication.models import User
from authentication.serializers import UserSerializer
from gestion_projet.models import Projects, Contributors, Issues
from gestion_projet.serializers import ProjectSerializer, InputProjectSerializer, ProjectsUserSerializer, IssueSerializer, InputIssueSerializer


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
        projects = Projects.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InputProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author=request.user)
            project_serializer = ProjectSerializer(project)
            return Response(project_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = InputProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # TODO : passer le ProjectSerializer
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response('Project Deleted', status=status.HTTP_200_OK)


class ProjectsUserList(APIView):
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
        serializer = ProjectsUserSerializer(data=request.data)
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteContributor(APIView):
    """
    Delete a contributor of the selected project.
    """
    # TODO : ajout permission isAuthor ?
    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id, user_id):
        try:
            contributor = Contributors.objects.get(user=user_id, project=project_id)
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
            issue = serializer.save(author_user_id=request.user, project_id=project)
            issue_serializer = IssueSerializer(issue)
            return Response(issue_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(APIView):
    """
    Update an issue or delete it.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, issue_id):
        issue = Issues.objects.get(pk=issue_id)
        print(issue.author_user_id)
        serializer = InputIssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            # TODO : trouver un autre moyen, si on ne veut pas changer le titre...
            issue = serializer.save(author_user_id=issue.author_user_id, project_id=issue.project_id )
            issue_serializer = IssueSerializer(issue)
            return Response(issue_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id):
        try:
            issue = Issues.objects.get(pk=issue_id, project_id=project_id)
            issue.delete()
            return Response(_("issue deleted of this project"))
        except Issues.DoesNotExist:
            raise Http404
