from django.contrib import admin
from shop.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
        "is_active",
    )
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "password",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "email",
        "first_name",
    )


admin.site.register(User, UserAdmin)
