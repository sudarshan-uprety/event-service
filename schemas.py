from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    product_id: str
    quantity: int


class InventoryProducer(BaseModel):
    operation: str
    products: List[Product]
