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

    def get(self, request, id=0):
        shopify_client = ShopifyClient()

        if id != 0:
            return JsonResponse(shopify_client.find_product(shopify_id=id).to_dict())
        else:
            all_products = []

            for collection in self.collections:
                products = shopify_client.retrieve_collection_products(
                    collection_id=self.collections[collection]
                )
                for product in products:
                    product_dict = product.to_dict()
                    product_dict['collection'] = collection
                    all_products.append(product_dict)

            return JsonResponse(all_products, safe=False)
