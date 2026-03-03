from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.validators import RegexValidator
from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        validators=[RegexValidator(r'^\d+$', 'Phone number must contain only digits.')]
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email
        
class ConfirmCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='confirm_codes')

    def __str__(self):
        return f'Код подтверждения для {self.user.email}'