from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.orders import (
    create_order, get_order, update_order_status, 
    get_all_orders
)

router = APIRouter(prefix="/api/orders", tags=["orders"])

class OrderItem(BaseModel):
    dish_id: str
    dish_name: str
    quantity: int
    unit_price: float

class CreateOrderRequest(BaseModel):
    customer_name: str
    phone: str
    items: List[OrderItem]

class OrderStatusUpdate(BaseModel):
    status: str

@router.post("")
async def place_order(request: CreateOrderRequest):
    """Place new order"""
    try:
        order = create_order(
            customer_name=request.customer_name,
            phone=request.phone,
            items=[item.dict() for item in request.items]
        )
        return order
    except Exception as e:
        print(f"ORDER ERROR: {str(e)}")  # Print to console
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/admin/all")
async def get_all_orders_admin():
    """Get all orders"""
    try:
        orders = get_all_orders()
        return orders
    except Exception as e:
        print(f"ORDER ERROR: {str(e)}")  # Print to console
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}")
async def get_order_status(order_id: str):
    """Get order details"""
    try:
        order = get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {str(e)}")  # Print to console
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{order_id}/status")
async def update_status(order_id: str, status_update: OrderStatusUpdate):
    """Update order status"""
    valid_statuses = ["Placed", "Confirmed", "Preparing", "Ready", "Picked Up"]
    
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status")
    
    try:
        order = update_order_status(order_id, status_update.status)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))