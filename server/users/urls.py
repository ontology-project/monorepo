from django.conf.urls import url
from .views import CustomTokenObtainPairView, UserRegistrationView

urlpatterns = [
    url('jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('auth/users/', UserRegistrationView.as_view(), name='user-registration'),
]