from django.db import models
from django_extensions.db.models import TimeStampedModel


class CollectionReminder(TimeStampedModel):
    shopify_id = models.BigIntegerField(
        blank=False,
        null=False,
        help_text="Shopify ID of the collection",
    )

    slug = models.SlugField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Slug of the collection for internal tracking only",
    )
