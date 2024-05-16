from django.contrib import admin

from .models import ProductReminder, CollectionReminder


@admin.register(CollectionReminder)
class CollectionReminderAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "shopify_id")


@admin.register(ProductReminder)
class ProductReminderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "shopify_id")
