# 2. Third-party
from django.apps import AppConfig


class KanbanAppConfig(AppConfig):
    """Configuration for the kanban app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kanban_app'
