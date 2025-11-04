from django.db import models


# 4. Brand
class Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)  # or ImageField if storing files

    def __str__(self):
        return self.name
