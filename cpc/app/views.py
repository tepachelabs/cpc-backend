from django.shortcuts import render


def index_view(request):
    return render(request, "app/index.html")


def privacy_view(request):
    return render(request, "app/privacy.html")
