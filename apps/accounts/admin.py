from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

@admin.register(Account)
class CustomAccountAdmin(UserAdmin):
    model = Account

    list_display = (
        "first_name",
        "last_name",
        "username",
        "email",
        "role",
        "phone_number",
        "is_active",
        "is_staff",
        "is_admin"
    )

    list_display_links = ("username", "email")
    
    list_filter = (
        "is_active",
        "is_staff",
        "is_admin",
        "is_superuser"
    )

    filter_horizontal = ("groups", "user_permissions")
    
    list_editable = ("is_staff", "is_active", "is_admin")

    readonly_fields = ("date_joined", "last_login")

    ordering = ("-date_joined",)

    fieldsets = (
        ("User Information",
            {
                "fields": ("username", "password")
            }
        ),
        ("Personal Information",
            {
                "fields": ("first_name", "last_name", "email", "phone_number")
            }
        ),
        ("Role",
            {
                "fields": ("role",)
            }
        ),
        ("Permissions", 
            {
                "fields": ("is_staff", "is_active", "is_admin")
            }
        ),
        ("Important Dates",
            {
                "fields": ("date_joined", "last_login")
            }
        ),
    )

    add_fieldsets = (
        (None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "role",
                    "username", 
                    "password1",
                    "password2",
                )
            }
        ),
    )
