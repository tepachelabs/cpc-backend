import os
import dj_database_url

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

from cpc.settings import BASE_DIR, PRODUCTION

# TODO change this to use the DATABASE_URL
DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
