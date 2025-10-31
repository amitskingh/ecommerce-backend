from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from ..managers.managers import UserManager


ROLE_CHOICES = [
    ("super_admin", "Super Admin"),
    ("admin", "Admin"),
    ("user", "User"),
]


# 2. Address
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

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country} - {self.postal_code}"
