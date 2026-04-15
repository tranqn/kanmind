# 2. Drittanbieter
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserInlineSerializer(serializers.ModelSerializer):
    """Nested user representation used in boards and tasks."""

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
