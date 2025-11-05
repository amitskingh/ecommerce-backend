from django.db import models


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
