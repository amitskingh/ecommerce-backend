from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .user import User
from .product import Product


# 14. Review
class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        limit_choices_to={"role": "USER"},
    )  # Assuming role field in User
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")  # One review per user per product

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
