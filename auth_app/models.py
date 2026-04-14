# 2. Drittanbieter
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with fullname field."""

    fullname = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

    def __str__(self):
        return self.email
