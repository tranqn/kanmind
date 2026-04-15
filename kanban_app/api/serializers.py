# 2. Drittanbieter
from django.contrib.auth import get_user_model
from rest_framework import serializers

# 3. Lokale Importe
from ..models import Board, Comment, Task

User = get_user_model()


class UserInlineSerializer(serializers.ModelSerializer):
    """Nested user representation used in boards and tasks."""

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardListSerializer(serializers.ModelSerializer):
    """Serializer for the board list view with computed counts."""

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


class BoardCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a board with member IDs."""

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()

    def create(self, validated_data):
        """Create board and assign owner and members."""
        members = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        board.members.set(members)
        return board


class TaskInlineSerializer(serializers.ModelSerializer):
    """Compact task serializer used inside board detail responses."""

    assignee = UserInlineSerializer(read_only=True)
    reviewer = UserInlineSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """Full board representation with members and tasks."""

    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = UserInlineSerializer(many=True, read_only=True)
    tasks = TaskInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardPatchSerializer(serializers.ModelSerializer):
    """Serializer for partial board updates (title and members)."""

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Board
        fields = ['title', 'members']

    def update(self, instance, validated_data):
        """Update title and replace member list."""
        members = validated_data.pop('members', None)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        if members is not None:
            instance.members.set(members)
        return instance

    def to_representation(self, instance):
        """Return full board data with nested owner and members after update."""
        return {
            'id': instance.id,
            'title': instance.title,
            'owner_data': UserInlineSerializer(instance.owner).data,
            'members_data': UserInlineSerializer(instance.members.all(), many=True).data,
        }


class TaskSerializer(serializers.ModelSerializer):
    """Full task serializer with nested user representations."""

    assignee = UserInlineSerializer(read_only=True)
    reviewer = UserInlineSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer', write_only=True, required=False, allow_null=True
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'assignee_id', 'reviewer', 'reviewer_id',
            'due_date', 'comments_count',
        ]
        read_only_fields = ['id', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for task comments with author fullname."""

    author = serializers.CharField(source='author.fullname', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']
