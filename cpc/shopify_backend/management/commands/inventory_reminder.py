from django.core.management.base import BaseCommand

from cpc.shopify_backend.tasks import inventory_reminder


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        inventory_reminder()
