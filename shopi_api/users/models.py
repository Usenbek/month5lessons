from django.db import models

# Create your models here.

class confirmcode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='confirm_codes')