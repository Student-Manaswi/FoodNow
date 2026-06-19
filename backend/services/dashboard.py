from config.db import get_orders_collection, get_feedback_collection
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

orders_col = get_orders_collection()
feedback_col = get_feedback_collection()

def get_dashboard_kpis() -> dict:
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Today's revenue
    today_orders = list(orders_col.find({"created_at": {"$gte": today}}))
    revenue = sum(o["total_price"] for o in today_orders)
    
    # Active orders by status
    active = orders_col.count_documents({"status": {"$in": ["Placed", "Confirmed", "Preparing", "Ready"]}})
    
    # Popular items
    all_items = []
    for order in today_orders:
        all_items.extend(order["items"])
    
    popular = {}
    for item in all_items:
        popular[item["dish_name"]] = popular.get(item["dish_name"], 0) + item["quantity"]
    
    top_5 = sorted(popular.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Avg feedback rating
    feedbacks = list(feedback_col.find())
    avg_rating = sum(f["rating"] for f in feedbacks) / len(feedbacks) if feedbacks else 0
    
    return {
        "today_revenue": revenue,
        "active_orders": active,
        "popular_items": [{"name": k, "count": v} for k, v in top_5],
        "avg_rating": round(avg_rating, 2)
    }