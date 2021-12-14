from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from .models import User
from .serializers import UserSerializer

# TODO : passer par une class APIView comme le reste de l'app
@api_view(['POST'])
def signup(request):
    # return Response('Utilisateur connecté')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        if not first_name:
            raise ValueError(_('first_name must be set'))

        last_name = request.POST.get('last_name')
        if not last_name:
            raise ValueError(_('last_name must be set'))

        email = request.POST.get('email')
        if not email:
            raise ValueError(_('email must be set'))

        password = request.POST.get('password')
        if not password:
            raise ValueError(_('password must be set'))

    user = User.objects.filter(email=email)
    if not user.exists():
        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password, 'salt', 'default')
        )
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return Response({"message": _(f'user {first_name} {last_name} created')})
    else:
        return Response({"message": _("le user n'a pas pu être créé")})
