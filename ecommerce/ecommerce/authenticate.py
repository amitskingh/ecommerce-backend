# from django.contrib.auth import authenticate
# from rest_framework import exceptions
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     username_field = "email"

#     def validate(self, attrs):
#         credentials = {"email": attrs.get("email"), "password": attrs.get("password")}

#         user = authenticate(**credentials)

#         if user:
#             if not user.is_active:
#                 raise exceptions.AuthenticationFailed("User is deactivated")

#             data = {}
#             refresh = self.get_token(user)

#             data["refresh"] = str(refresh)
#             data["access"] = str(refresh.access_token)

#             return data
#         else:
#             raise exceptions.AuthenticationFailed(
#                 "No active account found with the given credentials"
#             )


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
