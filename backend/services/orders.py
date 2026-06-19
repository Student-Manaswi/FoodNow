from config.db import get_orders_collection
from datetime import datetime, timezone
import uuid

orders_collection = get_orders_collection()

def create_order(customer_name: str, phone: str, items: list) -> dict:
    """Create new order"""
    total = sum(item.get("quantity", 0) * item.get("unit_price", 0) for item in items)
    order_id = f"ORD_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{str(uuid.uuid4())[:6].upper()}"
    
    order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "phone": phone,
        "items": items,
        "total_price": total,
        "status": "Placed",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    result = orders_collection.insert_one(order)
    order["_id"] = str(result.inserted_id)
    return serialize_doc(order)

def get_order(order_id: str) -> dict:
    """Get order by order_id"""
    result = orders_collection.find_one({"order_id": order_id})
    return serialize_doc(result)

def get_all_orders() -> list:
    """Get all orders (for admin)"""
    orders = list(orders_collection.find({}).sort("created_at", -1))
    return [serialize_doc(order) for order in orders]

def update_order_status(order_id: str, status: str) -> dict:
    """Update order status"""
    orders_collection.update_one(
        {"order_id": order_id},
        {"$set": {"status": status, "updated_at": datetime.now(timezone.utc)}}
    )
    return get_order(order_id)

def serialize_doc(doc):
    """Convert MongoDB document to response format"""
    if doc is None:
        return None
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    if "created_at" in doc and isinstance(doc["created_at"], datetime):
        doc["created_at"] = doc["created_at"].isoformat()
    if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
        doc["updated_at"] = doc["updated_at"].isoformat()
    return doc