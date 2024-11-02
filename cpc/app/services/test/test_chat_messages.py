from unittest import TestCase
from unittest.mock import Mock

from cpc import settings
from cpc.app.services.chat_messages import NewOrderChatMessageService
from cpc.shopify_backend.data import OrderCreateData, OrderCreateLineItemData


class TestNewOrderChatMessageService(TestCase):
    def test_send_message(self):
        telegram_service_mock = Mock()
        service = NewOrderChatMessageService()
        service.telegram_service = telegram_service_mock

        # Mock order data
        order_data = OrderCreateData(
            is_local_pickup=True,
            order_create_line_items=[
                OrderCreateLineItemData(
                    name="Café Chiapas",
                    price="150.00",
                    product_id=1,
                    product_name="Café",
                    quantity=2,
                    variant_name="Medio kilo",
                ),
                OrderCreateLineItemData(
                    name="Café Veracruz",
                    price="120.00",
                    product_id=2,
                    product_name="Café",
                    quantity=1,
                    variant_name="Un kilo",
                ),
            ],
            order_id=12345,
            order_number=67890,
            total_price="420.00",
            customer_name="Juan Pérez",
        )

        service.send_message(order_data)

        expected_message = (
            "📦 *Nueva Orden Web Recibida*: 67890\n\n"
            "💰 *Total*: $420\\.00\n"
            "🔖 *Etiquetar para*: Juan Pérez\n\n"
            "*Artículos en la Orden:*\n"
            "\\- Café Chiapas x2 \\(Medio kilo\\)\n"
            "\\- Café Veracruz x1 \\(Un kilo\\)\n"
            "\n"
            "✨ *Iran por él 🏠🚶🏼‍♂️*\n"
        )

        telegram_service_mock.send_message.assert_called_once_with(
            expected_message,
            message_thread_id=settings.TELEGRAM_ORDERS_MESSAGE_THREAD_ID,
            reply_markup={
                "inline_keyboard": [
                    [
                        {
                            "text": "📦 Shopify Admin",
                            "url": f"{settings.SHOPIFY_ADMIN_URL}/orders/12345",
                        }
                    ]
                ]
            },
        )
