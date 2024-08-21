from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("privacy", views.privacy_view, name="privacy-politic"),

    # API
    path("api/products", views.ProductsView.as_view()),
]
