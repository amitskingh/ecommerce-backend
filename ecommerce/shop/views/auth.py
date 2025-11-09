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
from django.core.mail import send_mail
from django.conf import settings

from ..utils.response_wrapper import success_response, error_response

from ..serializers.auth import RegisterUserSerializer, LoginUserSerializer


class RegisterUserView(APIView):
    """Register a new user with role"""

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return success_response(
                data={
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
                message="User registered successfully",
                status_code=status.HTTP_201_CREATED,
            )

        return error_response(
            message="User registration failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class LoginUserView(APIView):
    """Login a user and return JWT tokens"""

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(request, email=email, password=password)

            print("User: ", user)
            print("user role: ", user.role)

            if user and user.is_active:
                refresh = RefreshToken.for_user(user)
                print("valid user: ", user.first_name)

                return success_response(
                    data={
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
                    message="Login successful",
                    status_code=status.HTTP_200_OK,
                )

        return error_response(
            message="Invalid credentials",
            errors="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class RefreshTokenView(APIView):
    """Refresh access token"""

    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:

            return success_response(
                message="Refresh token is required",
                errors="Refresh token is required",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)

            return success_response(
                data={
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                message="Token refreshed successfully",
                status_code=status.HTTP_200_OK,
            )

        except Exception:

            return error_response(
                message="Invalid refresh token",
                errors="Invalid or expired refresh token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutUserView(APIView):
    """Logout user"""

    permission_classes = [IsAuthenticated]

    def post(self, request):

        return success_response(
            message="Logout successful",
            status_code=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    """Get current authenticated user information"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return success_response(
            data={
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                }
            },
            message="User data fetched successfully",
            status_code=status.HTTP_200_OK,
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

            return success_response(
                message="Password reset link sent successfully",
                status_code=status.HTTP_200_OK,
            )

        else:
            return error_response(
                message="User with credentials not found",
                errors="User with credentials not found",
                status_code=status.HTTP_404_NOT_FOUND,
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

            return error_response(
                message="Passwords do not match",
                errors="Passwords do not match",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return error_response(
                message="Invalid token",
                errors="Invalid token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data["new_password"])
            user.save()

            reset_obj.delete()

            return success_response(
                message="Password updated successfully",
                status_code=status.HTTP_200_OK,
            )

        else:

            return error_response(
                message="No user found",
                errors="No user found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
