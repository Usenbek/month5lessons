import random
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserCreateSerializer, UserAuthSerializer, ConfirmcodeSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode, CustomUser



@swagger_auto_schema(
    method='post',
    request_body=UserAuthSerializer,
    responses={200: openapi.Response('Token returned')}
)
@api_view(http_method_names=['POST'])
def authorization_api_view(request):

    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')

    user = authenticate(email=email, password=password)
    
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(status=status.HTTP_200_OK, data={"token": token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "Invalid credentials"})

 

@swagger_auto_schema(
    method='post',
    request_body=UserCreateSerializer,
    responses={201: openapi.Response('User created')}
)
@api_view(http_method_names=['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')

    with transaction.atomic():
        user = CustomUser.objects.create_user(email=email, password=password, is_active=False)
    
    code = str(random.randint(100000, 999999))
    ConfirmCode.objects.create(user=user, code=code)

    return Response(status=status.HTTP_201_CREATED, data={"user_id": user.id, "confirmation_code": code})


@swagger_auto_schema(
    method='post',  
    request_body=ConfirmcodeSerializer,
    responses={200: openapi.Response('User confirmed')}
)
@api_view(http_method_names=['POST'])
def confirm_code_api_view(request):
    user_id = request.data.get('user_id')
    code = request.data.get('code')
    try:
        confirm = ConfirmCode.objects.get(user_id=user_id, code=code)
    except ConfirmCode.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Invalid code"})
    
    user = confirm.user
    user.is_active = True
    user.save()
    ConfirmCode.objects.filter(user_id=user_id).delete()
    # create or get token for the user and return it
    token, _ = Token.objects.get_or_create(user=user)
    return Response(status=status.HTTP_200_OK, data={"message": "User confirmed", "token": token.key})

