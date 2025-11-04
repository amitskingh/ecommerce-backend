from django.db import models
from .product import Product
from .user import User


# 9. Coupon
class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ("PERCENT", "Percentage"),
        ("FIXED", "Fixed Amount"),
    )

    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    expiry_date = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(null=True, blank=True)  # None = unlimited
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_coupons"
    )
    used_count = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.code

    def is_valid(self, order_amount=None):
        from django.utils import timezone

        now = timezone.now()
        if self.expiry_date < now:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        if order_amount and order_amount < self.min_amount:
            return False
        return True
