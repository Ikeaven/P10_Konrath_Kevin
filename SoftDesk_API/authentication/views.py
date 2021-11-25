from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

# TODO: pas besoin de récupérer les users dans ce projet - A supprimer !!
class UserAPIView(APIView):

    def get(self, *args, **kwargs):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def signup(request):
    # return Response('Utilisateur connecté')
    if request.method == 'POST':
        # TODO vérifier la présence de tous les éléments ci dessous :
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')


    user = User.objects.filter(email=email)
    print('1')
    if not user.exists():
        print('2')
        # le user n'existe pas on peut le créer
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            password=make_password(password, 'salt', 'default')
        )
        print('TEST')
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return Response({"message": "Hello, world!"})
    else:
        return Response({"message":"le user n'a pas pu être créé"})