from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        SUPERADMIN = "SUPERADMIN", "SuperAdmin"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.ADMIN)

    def is_superadmin(self):
        return self.role == self.Roles.SUPERADMIN

    def is_admin(self):
        return self.role == self.Roles.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
