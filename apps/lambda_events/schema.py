from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    product_id: str
    quantity: int


class InventoryProducer(BaseModel):
    trace_id: str
    event_name: str
    products: List[Product]
