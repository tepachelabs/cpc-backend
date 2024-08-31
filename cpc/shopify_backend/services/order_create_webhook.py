import logging
from typing import Optional

from cpc.app.services.chat_messages import NewOrderChatMessageService
from cpc.shopify_backend.data import OrderCreateData, OrderCreateLineItemData
from cpc.shopify_backend.errors import ShopifyWebhookException

logger = logging.getLogger(__name__)


class OrderCreateDataService:
    @staticmethod
    def parse(data: dict):
        if data.get("source_name") != "web":
            logger.info("Order created from other source, ignoring webhook.")
            return

        # log all orders but we could check if the order is in a given collection in the future...
        logger.info("Order created from web, processing webhook data.")
        shipping_lines = data.get("shipping_lines", [])
        order_id: Optional[int] = data.get("id", None)
        if len(shipping_lines) == 0:
            logger.error(
                f"No shipping information found in order: {order_id}",
                extra={"data": data},
            )
            return
        if len(shipping_lines) > 1:
            logger.error(
                f"More than one shipping line found in order: {order_id}",
                extra={"data": data},
            )
            return
        shipping_line = shipping_lines[0]
        local_pickup = shipping_line.get("code") == "Shop location"

        total_price: Optional[str] = data.get("total_price", None)
        order_number: Optional[int] = data.get("order_number", None)
        customer: Optional[dict] = data.get("customer", None)
        customer_name: Optional[str] = None
        if customer is not None:
            customer_name = (
                f"{customer.get('first_name', '')} {customer.get('last_name', '')}"
            )
        if any(x is None for x in (order_id, total_price, order_number)):
            raise ShopifyWebhookException(f"Order data missing in webhook data")

        line_items = data.get("line_items", [])
        order_items = []
        for line_item in line_items:
            product_id = line_item.get("product_id", None)
            product_name = line_item.get("title", None)
            quantity = line_item.get("quantity", None)
            variant_id = line_item.get("variant_id", None)
            variant_name = line_item.get("variant_title", None)
            price = line_item.get("price", None)
            if any(x is None for x in (product_id, product_name, quantity, price)):
                raise ShopifyWebhookException(
                    f"Missing line item data in order: {order_id}"
                )
            order_items.append(
                OrderCreateLineItemData(
                    name=product_name,
                    price=price,
                    product_id=product_id,
                    product_name=product_name,
                    quantity=quantity,
                    variant_id=variant_id,
                    variant_name=variant_name,
                )
            )
        return OrderCreateData(
            order_id=order_id,
            is_local_pickup=local_pickup,
            total_price=total_price,
            order_create_line_items=order_items,
            order_number=order_number,
            customer_name=customer_name,
        )


class OrderCreateWebhookService:
    data_service = OrderCreateDataService()
    new_order_chat_message_service = NewOrderChatMessageService()

    def process(self, data: dict):
        order_data: Optional[OrderCreateData] = self.data_service.parse(data)
        if order_data is None:
            return

        self.new_order_chat_message_service.send_message(order_data)
        return order_data
