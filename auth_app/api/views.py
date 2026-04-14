# 2. Drittanbieter
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Lokale Importe
from .serializers import LoginSerializer, RegistrationSerializer, UserBasicSerializer

User = get_user_model()


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


class EmailCheckView(APIView):
    """Check if an email address belongs to a registered user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return user data if email exists, 404 otherwise."""
        email = request.query_params.get('email')
        if not email:
            return Response({'detail': 'Email parameter required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserBasicSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
