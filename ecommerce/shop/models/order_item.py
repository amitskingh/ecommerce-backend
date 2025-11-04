from django.db import models
from .order import Order
from .product_variant import ProductVariant


# 13. OrderItem
class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=12, decimal_places=2
    )  # Snapshot of price at purchase

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.name}"
