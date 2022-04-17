from rest_framework.serializers import ModelSerializer
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from models import Lobby, User
from accord.models import Lobby, User



class LobbySerializer(ModelSerializer):
    class Meta:
        model = Lobby
        fields = '__all__'



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['password']



class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password',]

# class UserSerializer