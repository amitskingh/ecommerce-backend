from django.db import models
from .product import Product
from .user import User


# 8. Discount
class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ("PERCENT", "Percentage"),
        ("FIXED", "Fixed Amount"),
    )

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_discounts"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
