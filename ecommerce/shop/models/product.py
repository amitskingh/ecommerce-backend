from django.db import models
from .__init__ import User, Category, Brand
from django.utils.text import slugify


# 6. Product
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_products"
    )
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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
