# 2. Drittanbieter
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Lokale Importe
from ..models import Board, Task
from .permissions import (
    IsBoardMemberOrOwner,
    IsBoardOwner,
    IsTaskBoardMember,
    IsTaskCreatorOrBoardOwner,
)
from .serializers import (
    BoardCreateSerializer,
    BoardDetailSerializer,
    BoardListSerializer,
    BoardPatchSerializer,
    TaskSerializer,
)


class BoardListCreateView(APIView):
    """List boards for the current user or create a new one."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return boards where user is owner or member."""
        boards = Board.objects.filter(
            owner=request.user
        ) | Board.objects.filter(members=request.user)
        boards = boards.distinct()
        serializer = BoardListSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new board with the current user as owner."""
        serializer = BoardCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner=request.user)
        return Response(BoardCreateSerializer(board).data, status=status.HTTP_201_CREATED)


class BoardDetailView(APIView):
    """Retrieve, update, or delete a single board."""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Fetch board or return None."""
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return None

    def get(self, request, board_id):
        """Return board detail with tasks."""
        board = self.get_object(board_id)
        if board is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, board)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, board_id):
        """Update board title and members."""
        board = self.get_object(board_id)
        if board is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, board)
        serializer = BoardPatchSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        return Response(BoardPatchSerializer(updated).to_representation(updated), status=status.HTTP_200_OK)

    def delete(self, request, board_id):
        """Delete board — only owner allowed."""
        board = self.get_object(board_id)
        if board is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, board)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """Assign stricter permissions for delete."""
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardMemberOrOwner()]


class AssignedToMeView(ListAPIView):
    """Return tasks where the current user is the assignee."""

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class ReviewingView(ListAPIView):
    """Return tasks where the current user is the reviewer."""

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class TaskCreateView(APIView):
    """Create a new task inside a board."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create task if user is a board member."""
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.validated_data.get('board')
        if board is None:
            return Response({'detail': 'Board required.'}, status=status.HTTP_400_BAD_REQUEST)
        is_member = board.members.filter(id=request.user.id).exists()
        is_owner = board.owner == request.user
        if not (is_member or is_owner):
            return Response({'detail': 'You must be a board member.'}, status=status.HTTP_403_FORBIDDEN)
        task = serializer.save(created_by=request.user)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    """Update or delete a single task."""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Fetch task or return None."""
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def patch(self, request, task_id):
        """Update task fields; board reassignment is not allowed."""
        task = self.get_object(task_id)
        if task is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, task)
        if 'board' in request.data:
            return Response({'detail': 'Changing board is not allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, task_id):
        """Delete task — only creator or board owner allowed."""
        task = self.get_object(task_id)
        if task is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """Assign delete-specific permissions."""
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsTaskBoardMember()]
