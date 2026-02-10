import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserCreateSerializer, UserAuthSerializer
from rest_framework import status
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import confirmcode

@api_view(http_method_names=['POST'])
def authorization_api_view(request):

    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(status=status.HTTP_200_OK, data={"token": token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "Invalid credentials"})
 
# Create your views here.
@api_view(http_method_names=['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password, is_active=False)
    
    code = str(random.randint(100000, 999999))
    confirmcode.objects.create(user=user, code=code)

    return Response(status=status.HTTP_201_CREATED, data={"user_id": user.id})


@api_view(http_method_names=['POST'])
def confirm_code_api_view(request):
    user_id = request.data.get('user_id')
    code = request.data.get('code')
    
    try:
        confirm = confirmcode.objects.get(user_id=user_id, code=code)
    except confirmcode.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Invalid code"})
    
    user = confirm.user
    user.is_active = True
    user.save()
    confirmcode.objects.filter(user_id=user_id).delete()
    return Response(status=status.HTTP_200_OK, data={"message": "User confirmed"})

