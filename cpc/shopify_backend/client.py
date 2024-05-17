import logging

# noinspection PyPackageRequirements
import shopify
from django.conf import settings
from pyactiveresource.connection import ResourceNotFound

logger = logging.getLogger(__name__)


class ShopifyClient:
    def __init__(
        self,
        shop_url=settings.SHOPIFY_SHOP_URL,
        access_token=settings.SHOPIFY_ACCESS_TOKEN,
        api_version=settings.SHOPIFY_API_VERSION,
        _shopify=shopify,
    ):
        self._shopify = _shopify
        session = self._shopify.Session(shop_url, api_version, access_token)
        self._shopify.ShopifyResource.activate_session(session)

    @property
    def active(self) -> bool:
        return self._shopify.Shop.current() is not None

    def find_collection(self, shopify_id: int):
        try:
            return self._shopify.CustomCollection.find(shopify_id)
        except ResourceNotFound as e:
            logger.warning(f"Collection not found: {e}")
            return None

    def find_product(self, **kwargs):
        try:
            shopify_id = kwargs.get("shopify_id", None)
            if shopify_id is not None:
                return self._shopify.Product.find(shopify_id)
            return self._shopify.Product.find_first(**kwargs)
        except ResourceNotFound as e:
            logger.warning(f"Product not found: {e}")
            return None
