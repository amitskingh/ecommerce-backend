from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..models import User, PasswordReset
from ..serializers.password_reset_request import PasswordResetRequestSerializer
from ..serializers.password_reset import PasswordResetSerializer


from rest_framework import generics
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os
from django.core.mail import send_mail
from django.conf import settings


class RegisterUserView(APIView):
    """Register a new user with role"""

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "user")  # Default role is user

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate role
        valid_roles = ["super_admin", "admin", "user"]
        if role not in valid_roles:
            return Response(
                {"error": f"Invalid role. Must be one of: {valid_roles}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(email=email, password=password, role=role)
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": role,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginUserView(APIView):
    """Login a user and return JWT tokens"""

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, email=email, password=password)

        print("User: ", user)
        print("user role: ", user.role)

        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            print("valid user: ", user.first_name)

            return Response(
                {
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "role": user.role,
                    },
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class RefreshTokenView(APIView):
    """Refresh access token"""

    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutUserView(APIView):
    """Logout user"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"message": "Logout successful. Please delete the token on client side."},
            status=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    """Get current authenticated user information"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()

            # reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}"
            reset_url = f"http://127.0.0.1:8000/api/v1/auth/password-reset/{token}"

            # Sending reset link via email (commented out for clarity)
            # ... (email sending code)

            subject = "Password Reset Request"
            message = f"Click the link below to reset your password:\n{reset_url}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [
                email,
            ]

            send_mail(subject, message, email_from, recipient_list)

            return Response(
                {
                    "success": "We have sent you a link to reset your password",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "User with credentials not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        new_password = data["new_password"]
        confirm_password = data["confirm_password"]

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({"error": "Invalid token"}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data["new_password"])
            user.save()

            reset_obj.delete()

            return Response({"success": "Password updated"})
        else:
            return Response({"error": "No user found"}, status=404)
