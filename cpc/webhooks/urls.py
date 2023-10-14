from django.urls import path
from . import views

urlpatterns = [
    path("gform/", views.GoogleFormWebhookView.as_view(), name="google_form_webhook"),
]
