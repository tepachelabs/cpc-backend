import json
import os
from unittest import TestCase

from cpc.shopify_backend.services import OrderCreateDataService


class TestOrderCreateWebhookService(TestCase):
    def setUp(self):
        self.order_create_data_service = OrderCreateDataService()

    def test_process__scenario(self):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(
            script_dir, "fixtures/order_create_webhook/shop_webhook.json"
        )
        with open(file_path) as f:
            data = json.load(f)

        result = self.order_create_data_service.parse(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.order_id, 5715617874001)
        self.assertEqual(result.order_number, 1006)
        self.assertEqual(result.total_price, "0.00")
        self.assertEqual(result.is_local_pickup, False)

    def test_process__local_pickup_scenario(self):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(
            script_dir,
            "fixtures/order_create_webhook/shop_webhook__with_local_pickup.json",
        )
        with open(file_path) as f:
            data = json.load(f)

        result = self.order_create_data_service.parse(data)
        self.assertEqual(result.is_local_pickup, True)

    def test_process__pos_scenario(self):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(
            script_dir,
            "fixtures/order_create_webhook/shop_webhook__from_other_source.json",
        )
        with open(file_path) as f:
            data = json.load(f)

        result = self.order_create_data_service.parse(data)
        self.assertIsNone(result)
