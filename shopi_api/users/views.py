import random
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserCreateSerializer, UserAuthSerializer, ConfirmcodeSerializer
from django.core.cache import cache
from .models import CustomUser, ConfirmCode
from common.permissions import IsOwner, IsAnonymous


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
        token, _ = Token.objects.get_or_create(user=user)
        return Response(status=status.HTTP_200_OK, data={"token": token.key})
    
    return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "Invalid credentials"})

@swagger_auto_schema(
    method='post',
    request_body=UserCreateSerializer,
    responses={201: openapi.Response('User created, code sent to email (for dev in response)')}
)
@api_view(['POST'])
def registration_api_view(request):
    from .tasks import add, show_time, send_test_email
    # add.delay(5, 7)
    # show_time.delay()
    # send_test_email.delay()
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')

    with transaction.atomic():
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_active=False
        )

    code = ''.join(random.choices('0123456789', k=6))
    
    return Response(status=status.HTTP_201_CREATED, data={"user_id": user.id,"confirm_code": code})

    # cache_key = f"otp:reg:{email}"

    # cache.set(cache_key, code, timeout=300)

    # return Response(
    #     status=status.HTTP_201_CREATED,
    #     data={
    #         "message": "User created. Confirm code sent.",
    #         "user_id": user.id,
    #         "dev_code": code 
    #     }
    # )

@swagger_auto_schema(
    method='post',
    request_body=ConfirmcodeSerializer,
    responses={
        200: openapi.Response('User confirmed, token returned'),
        400: openapi.Response('Invalid or expired code'),
    }
)
@api_view(['POST'])
def confirm_code_api_view(request):
    user_id = request.data.get('user_id')
    code = request.data.get('code')

    if not user_id or not code:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"error": "user_id and code are required"}
        )

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"error": "User not found"}
        )


    cache_key = f"otp:reg:{user.email}"

    saved_code = cache.get(cache_key)
    if saved_code is None:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"error": "Код истёк или не существует"}
        )

    if saved_code != str(code):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"error": "Неверный код"}
        )

    cache.delete(cache_key)

    user.is_active = True
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        status=status.HTTP_200_OK,
        data={
            "message": "Пользователь подтверждён",
            "token": token.key
        }
    )