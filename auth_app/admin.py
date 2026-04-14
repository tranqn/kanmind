# 2. Drittanbieter
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# 3. Lokale Importe
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser."""

    list_display = ['id', 'email', 'fullname', 'is_active', 'is_staff']
    search_fields = ['email', 'fullname']
    ordering = ['id']
