# 2. Drittanbieter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Lokale Importe
from ..models import Board
from .serializers import BoardCreateSerializer, BoardListSerializer


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
