from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id','email', 'phone_number', 'is_active', 'is_superuser')
    ordering = ('email',)
    
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                (None, {'fields': ('email', 'password', 'phone_number')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                ('Important dates', {'fields': ('last_login',)}),
            )
        return (
            (None, {'fields': ('email', 'password')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login',)}),
        )
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['email', 'password'] 