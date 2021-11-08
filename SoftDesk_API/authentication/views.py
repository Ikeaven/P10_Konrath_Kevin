from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers import UserSerializer

# TODO: pas besoin de récupérer les users dans ce projet - A supprimer !!
class UserAPIView(APIView):

    def get(self, *args, **kwargs):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)