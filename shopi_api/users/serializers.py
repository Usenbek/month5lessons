from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class UserAuthSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)



class UserCreateSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(default=False)

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


    def validate_username(self,username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("This username is already taken")