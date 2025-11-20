from django.db import models
from .user import User


STATUS_CHOICES = [
    ("pending", "Pending"),
    ("paid", "Paid"),
]


# Fine Model
class Fine(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fines")
    stripe_account_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Fine: {self.name} for {self.user.username}"
