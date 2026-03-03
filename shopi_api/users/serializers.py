from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import CustomUser, ConfirmCode

class UserAuthSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)



class UserCreateSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(default=False)

    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_email(self,email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError("This email is already taken")
    
    def validate_phone_number(self, value):
        request = self.context.get('request')
        if value and request and request.user and not request.user.is_superuser:
            raise ValidationError("Only superusers can set phone_number")
        return value
    

class ConfirmcodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)