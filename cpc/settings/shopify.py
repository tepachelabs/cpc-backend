import os

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", None)
SHOPIFY_SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME", None)
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-01")

SHOPIFY_SHOP_URL = (
    f"https://{SHOPIFY_SHOP_NAME}.myshopify.com" if SHOPIFY_SHOP_NAME else None
)

SHOPIFY_ADMIN_URL = (
    f"https://admin.shopify.com/store/{SHOPIFY_SHOP_NAME}"
    if SHOPIFY_SHOP_NAME
    else None
)

SHOPIFY_WEBHOOK_SECRET = os.getenv("SHOPIFY_WEBHOOK_SECRET", None)
