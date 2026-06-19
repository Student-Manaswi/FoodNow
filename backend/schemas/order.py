from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    dish_id: str
    dish_name: str
    quantity: int
    unit_price: float

class CreateOrder(BaseModel):
    customer_name: str
    phone: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str
    order_id: str
    customer_name: str
    phone: str
    items: List[OrderItem]
    total_price: float
    status: str
    created_at: str