from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        TECHNICIAN = "technician", "Technician"
        SALES = "sales_agent", "SalesAgent"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.SALES)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser

    def is_technician(self):
        return self.role == self.Roles.TECHNICIAN

    def is_sales(self):
        return self.role == self.Roles.SALES
