from django.db import models
from django_extensions.db.models import TimeStampedModel


class Reminder(TimeStampedModel):
    slug = models.SlugField(max_length=255)
    message = models.TextField()
