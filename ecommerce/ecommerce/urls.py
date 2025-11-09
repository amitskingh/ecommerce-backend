"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# ecommerce/urls.py   <-- make sure this is your root urls file
from django.contrib import admin
from django.urls import path, include
from shop.utils.response_wrapper import success_response, error_response

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("shop.urls")),
]


# def custom_page_not_found(request, exception):
#     # handler404 must accept (request, exception)
#     return error_response(
#         message="Endpoint not found",
#         errors=None,
#         status_code=404,
#     )


# def custom_server_error(request):
#     # handler500 must accept only (request)
#     return error_response(
#         message="Internal server error",
#         errors=None,
#         status_code=500,
#     )


# handler404 = "ecommerce.urls.custom_page_not_found"
# handler500 = "ecommerce.urls.custom_server_error"
