# 2. Third-party
from django.contrib import admin

# 3. Local imports
from .models import Board, Comment, Task


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Admin configuration for Board."""

    list_display = ['id', 'title', 'owner']
    search_fields = ['title', 'owner__email']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task."""

    list_display = [
        'id',
        'title',
        'board',
        'status',
        'priority',
        'assignee',
        'reviewer']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'board__title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment."""

    list_display = ['id', 'task', 'author', 'created_at']
    search_fields = ['author__email', 'task__title']
