from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import MyAccountManager

class RoleChoices(models.TextChoices):
    CUSTOMER = "Customer"
    SELLER = "Seller"
    ADMIN = "Admin"

class Account(AbstractBaseUser, PermissionsMixin):
    """
    This is the account model for the application.
    Authentication is performed using email instead of username
    """
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    phone_number = models.CharField(max_length=20)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_number"]

    objects = MyAccountManager()

    # This will return the email
    def __str__(self):
        return self.email

    # This is for checking permission
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
