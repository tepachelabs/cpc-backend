from django.urls import path
from . import views

urlpatterns = [
    path(
        "admin-webhook", views.AdminWebhookView.as_view(), name="shopify_admin_webhook"
    ),
]
