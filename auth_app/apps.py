# 2. Drittanbieter
from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Configuration for the authentication app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'
