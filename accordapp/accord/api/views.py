from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accord.models import Lobby, User
from rest_framework.views import APIView

from .serializers import *

@api_view(['GET'])
def getRouts(request):
    routs = [
        'GET /api',
        'GET /api/lobbys',
        'GET /api/lobbys/:id'
    ]

    return Response(routs)


@api_view(['GET'])
def getLobbys(request):
    lobbys = Lobby.objects.all()
    serializer = LobbySerializer(lobbys, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getLobby(request, pk):
    lobby = Lobby.objects.get(id=pk)
    serializer = LobbySerializer(lobby, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# @csrf_exempt
class Userlogin(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


    def get(self, request):
        user = User.objects.all()
        serializer = LobbySerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = User.objects.get(email=request.data['email'])
            return Response(user.username, status=200)
        else:
            return Response(status=400)


# @api_view(['POST'])
# def userlogin(request):
#     serializer = LoginSerializer(data=request.data)
#     print(serializer)
#     # user = authenticate(request, serializer=serializer)
#     # print(user)
#     # print(serializer.is_valid())
#     if serializer.is_valid():
#         print('valid')
#         # user = serializer.validated_data['user']
#         # login(request, user)
#         return Response(serializer.data)
#     else:
#         return Response('bhai hoy nai')

    # permission_classes = (AllowAny,)
    # serilaizer = LoginSerializer