from django.contrib import admin

from .models import CollectionReminder


@admin.register(CollectionReminder)
class CollectionReminderAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "shopify_id")
