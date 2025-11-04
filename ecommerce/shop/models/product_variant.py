from django.db import models
from .product import Product

# 7. ProductVariant
# One product can have multiple variants (e.g., different sizes, colors)
# Product to ProductVariant is One-to-Many
class ProductVariant(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)  # e.g., "Red - XL"
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (
            "product",
            "name",
        )  # Optional: ensure unique variant names per product

    def __str__(self):
        return f"{self.product.name} - {self.name}"
