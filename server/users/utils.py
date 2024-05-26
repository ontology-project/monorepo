from djoser.serializers import UserSerializer
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import CustomUserSerializer

def custom_jwt_response_handler(token, user=None, request=None):
    return {
        'access': str(token.access_token),
        'refresh': str(token),
        'user': CustomUserSerializer(user, context={'request': request}).data
    }


def custom_jwt_response_handler(token, user=None, request=None):
    return {
        'access': token,
        'user': CustomUserSerializer(user, context={'request': request}).data
    }
