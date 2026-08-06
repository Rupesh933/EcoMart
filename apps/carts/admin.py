from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

@admin.register(Cart)
class CustomCartAdmin(admin.ModelAdmin):
    list_display = (
        "cart_id",
        "date_added"
    )

    list_filter = (
        "cart_id",
        "date_added"
    )

    ordering = ("-date_added",)

    search_fields = (
        "cart_id",
    )

    

@admin.register(CartItem)
class CustomCartItemAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "cart",
        "quantity"
    )

    list_filter = (
        "cart",
        "quantity"
    )

    ordering = ("-cart",)