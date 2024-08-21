from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from cpc.shopify_backend.client import ShopifyClient


def index_view(request):
    return render(request, "app/index.html")


def privacy_view(request):
    return render(request, "app/privacy.html")


class ProductsView(APIView):
    collections = {
        "coffee": 479837782309,
        "misc": 479838044453,
        "merch": 479838241061,
    }

    def get(self, request):
        shopify_client = ShopifyClient()

        products = {}

        for collection in self.collections:
            products[collection] = shopify_client.retrieve_collection_products(
                collection_id=self.collections[collection]
            )

        return JsonResponse({
            collection: [p.to_dict() for p in products[collection]]
            for collection in self.collections
        })

    def post(self, request):
        return render(request, "app/index.html")
