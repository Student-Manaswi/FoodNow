from fastapi import APIRouter, Query
from services.search import vector_search
from schemas.search import SearchQuery, DishResponse
from schemas.order import CreateOrder
from schemas.feedback import CreateFeedback
from schemas.menu import DishCreate, UpdateDish
from services.orders import create_order, get_order, update_order_status
from services.feedback import create_feedback, get_all_feedback
from services.dashboard import get_dashboard_kpis
from services.menu import create_dish, update_dish, delete_dish
from services.recommendations import get_recommendations
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api", tags=["spiceroute"])


# ─── SEARCH ───────────────────────────────────────────────────────────────────

@router.post("/search", response_model=List[DishResponse])
def ai_search(
    query: str = Query(..., description="Natural language search query"),
    max_price: float = Query(None, description="Max price filter"),
    category: str = Query(None, description="Category filter")
):
    """AI-powered semantic menu search"""
    results = vector_search(query, max_price, category)
    return results


from config.db import get_dishes_collection

from fastapi import APIRouter, Query
from schemas.search import DishResponse
from config.db import get_dishes_collection
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api", tags=["spiceroute"])

# ─── SEARCH & PAGE LOAD ───────────────────────────────────────────────────────

@router.get("/search", response_model=List[DishResponse])
def get_all_dishes(category: Optional[str] = Query(None)):
    """Fetches all dishes safely for the initial page load using the secure client"""
    dishes_collection = get_dishes_collection()
    query = {}

    if category and category.strip() != "" and category.lower() != "all":
        query["category"] = {"$regex": f"^{category.strip()}$", "$options": "i"}

    try:
        results = list(dishes_collection.find(query))
    except Exception as e:
        print(f"❌ DB Fetch Failed: {e}")
        results = []

    return [
        DishResponse(
            id=str(r["_id"]),
            name=r["name"],
            description=r["description"],
            price=r["price"],
            category=r["category"],
            dietary_tags=r["dietary_tags"],
            is_available=r.get("is_available", True),
            image_url=r.get("image_url")
        )
        for r in results
    ]
# ─── CART / RECOMMENDATIONS ───────────────────────────────────────────────────

class CartItem(BaseModel):
    dish_id: Optional[str] = None
    name: Optional[str] = None
    dietary_tags: List[str]


@router.post("/cart/recommend")
def recommend(items: List[CartItem]):
    """Get cross-sell recommendation based on cart items"""
    result = get_recommendations([item.dict() for item in items])
    return result


# ─── ORDERS ───────────────────────────────────────────────────────────────────

@router.post("/orders")
def place_order(order: CreateOrder):
    result = create_order(
        order.customer_name,
        order.phone,
        [item.dict() for item in order.items]
    )
    return result


@router.get("/orders/{order_id}")
def get_order_details(order_id: str):
    return get_order(order_id)


@router.patch("/orders/{order_id}/status")
def update_status(order_id: str, status: str):
    return update_order_status(order_id, status)


# ─── FEEDBACK ─────────────────────────────────────────────────────────────────

@router.post("/feedback")
def submit_feedback(feedback: CreateFeedback):
    return create_feedback(feedback.order_id, feedback.rating, feedback.comment)


@router.get("/feedback")
def get_feedback():
    return get_all_feedback()


# ─── ADMIN DASHBOARD ──────────────────────────────────────────────────────────

@router.get("/admin/dashboard")
def dashboard():
    return get_dashboard_kpis()


# ─── ADMIN MENU CRUD ──────────────────────────────────────────────────────────

@router.post("/admin/dishes")
def add_dish(dish: DishCreate):
    return create_dish(
        dish.name,
        dish.description,
        dish.category,
        dish.price,
        dish.dietary_tags
    )


@router.patch("/admin/dishes/{dish_id}")
def edit_dish(dish_id: str, dish: UpdateDish):
    return update_dish(dish_id, dish.dict(exclude_unset=True))


@router.delete("/admin/dishes/{dish_id}")
def remove_dish(dish_id: str):
    return {"deleted": delete_dish(dish_id)}

from services.orders import get_all_orders

@router.get("/orders")
def list_orders():
    return get_all_orders()