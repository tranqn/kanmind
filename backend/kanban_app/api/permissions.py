# 2. Third-party
from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    """Allow access only to board members or the board owner."""

    def has_object_permission(self, request, view, obj):
        """Check membership or ownership on a Board instance."""
        return obj.owner == request.user or obj.members.filter(
            id=request.user.id).exists()


class IsBoardOwner(BasePermission):
    """Allow access only to the board owner."""

    def has_object_permission(self, request, view, obj):
        """Check ownership on a Board instance."""
        return obj.owner == request.user


class IsTaskBoardMember(BasePermission):
    """Allow access only to members of the board a task belongs to."""

    def has_object_permission(self, request, view, obj):
        """Check if user is member or owner of the task's board."""
        board = obj.board
        return board.owner == request.user or board.members.filter(
            id=request.user.id).exists()


class IsTaskCreatorOrBoardOwner(BasePermission):
    """Allow delete only to task creator or board owner."""

    def has_object_permission(self, request, view, obj):
        """Check if user created the task or owns its board."""
        return (
            obj.created_by == request.user
            or obj.board.owner == request.user
        )


class IsCommentAuthor(BasePermission):
    """Allow delete only to the comment author."""

    def has_object_permission(self, request, view, obj):
        """Check if user is the comment author."""
        return obj.author == request.user
