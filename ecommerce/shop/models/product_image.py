from django.db import models
from .product import Product


# 6. ProductImage
# One product can have multiple images
# Product to ProductImage is One-to-Many
class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image_url = models.URLField()  # or ImageField

    def __str__(self):
        return f"Image for {self.product.name}"
