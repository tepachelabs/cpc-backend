import dataclasses
from typing import Optional


@dataclasses.dataclass
class OrderCreateLineItemData:
    name: str
    price: str
    product_id: int
    product_name: str
    quantity: int
    variant_id: Optional[int] = None
    variant_name: Optional[str] = None


@dataclasses.dataclass
class OrderCreateData:
    is_local_pickup: bool
    order_create_line_items: list[OrderCreateLineItemData]
    order_id: int
    order_number: int
    total_price: str
    customer_name: Optional[str] = None
