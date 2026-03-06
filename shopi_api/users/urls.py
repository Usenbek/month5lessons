from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,
    TokenVerifyView   
)
from .serializers import CustomTokenObtainPairSerializer
urlpatterns = [
    path('registration/', views.registration_api_view),
    path('confirm/', views.confirm_code_api_view),
    path('login/', views.authorization_api_view),
    path("api/v1/jwt/", TokenObtainPairView.as_view(serializer_class = CustomTokenObtainPairSerializer), name="token_obtain_pair"),
    path("api/v1/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
]