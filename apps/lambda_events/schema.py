from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    product_id: str
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None


class InventoryProducer(BaseModel):
    trace_id: str
    event_name: str
    products: List[Product]
