from django.contrib import admin

from cpc.app.models.reminders import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("slug", "created", "modified")
