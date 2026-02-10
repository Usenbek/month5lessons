from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('confirm/', views.confirm_code_api_view),
    path('login/', views.authorization_api_view),
]