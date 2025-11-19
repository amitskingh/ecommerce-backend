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

    @property
    def is_seller(self):
        return self.role == "seller"

    @property
    def is_customer(self):
        return self.role == "customer"

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_staff

    @property
    def is_fully_onboarded(self):
        """Seller is ready to receive payouts"""
        return self.is_seller and self.charges_enabled and self.payouts_enabled

    objects = UserManager()

    ####################################################
    # STRIPE Configuration
    ####################################################

    # Stripe Customer (for charging anyone)
    stripe_customer_id = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )

    # Stripe Connect – only for sellers
    stripe_account_id = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )

    country = models.CharField(max_length=2, blank=True)  # e.g. "US"

    # Status flags (updated by webhook)
    charges_enabled = models.BooleanField(default=False)
    payouts_enabled = models.BooleanField(default=False)
    details_submitted = models.BooleanField(default=False)

    # Raw requirement data from Stripe (for UI)
    requirements = models.JSONField(default=dict, blank=True)
    capabilities = models.JSONField(default=dict, blank=True)

    # Optional nice-to-have
    onboarding_completed_at = models.DateTimeField(null=True, blank=True)
    last_webhook_at = models.DateTimeField(null=True, blank=True)

    ####################################################
    # STRIPE Configuration END
    ####################################################

    def __str__(self):
        return self.first_name + " " + self.last_name
