# 2. Drittanbieter
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Lokale Importe
from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(APIView):
    """Handle new user registration. Returns token on success."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user and return auth token."""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'fullname': user.fullname, 'email': user.email, 'user_id': user.id},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Authenticate a user and return an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Validate credentials via serializer and return token."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'fullname': user.fullname, 'email': user.email, 'user_id': user.id},
            status=status.HTTP_200_OK,
        )
