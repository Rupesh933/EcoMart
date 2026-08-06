from django.contrib import admin

from django.utils.html import format_html
from django.utils.text import Truncator

from .models import Product, Variation

@admin.register(Product)
class CustomProductAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "stock",
        "created_date",
        "modified_date",
        "is_available",
        "images_preview"
    )

    prepopulated_fields = {
        "slug": ("product_name",)
    }

    search_fields = (
        "product_name",
        "category__name",
    )

    list_filter = (
        "product_name",
        "price",
        "stock",
        "category",
        "created_date",
        "modified_date",
        "is_available"
    )

    ordering = ("-created_date",)

    def short_description(self, obj):
        return Truncator(obj.description).chars(20)

    def images_preview(self, obj):
        if obj.images:
            return format_html(
                '<img src="{}" width="80" height="60" '
                'style="object-fit:cover; border-radius:4px;" />',
                obj.images.url,
            )
        return "No Image"
    
    images_preview.short_description = "Image Preview"

@admin.register(Variation)
class CustomVariationAdmin(admin.ModelAdmin):
    list_display = (
        "product__product_name",
        "variation_category",
        "variation_value",
        "is_active"
    )
    list_filter = (
        "product",
        "variation_category",
        "variation_value",
        "is_active"
    )
    search_fields = (
        "product__product_name",
        "variation_category",
        "variation_value",
    )
    readonly_fields = (
        "created_date",
    )
