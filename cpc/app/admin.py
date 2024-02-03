from django.contrib import admin

from .models import ProductReminder


@admin.register(ProductReminder)
class ProductReminderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "shopify_id")
