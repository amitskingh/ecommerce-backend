from django.urls import path
from ..views.category import CategoryListView, CategoryDetailView


urlpatterns = [
    path(
        "categories/",
        CategoryListView.as_view(),
        name="register_user",
    ),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="register_user",
    ),
]
