from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from ..managers.managers import UserManager

ROLE_CHOICES = [
    ("admin", "Admin"),
    ("seller", "Seller"),
    ("customer", "Customer"),
]


# 1. User
class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    phone_number = models.CharField(max_length=15, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    profile_image = models.ImageField(null=True, upload_to="profile_image")

    role = models.CharField(
        max_length=11,
        choices=ROLE_CHOICES,
        default="user",
    )

    default_address = models.ForeignKey(
        "Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_for_user",
    )

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name
