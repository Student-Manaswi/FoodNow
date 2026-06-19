from fastapi import APIRouter, Query
from services.search import vector_search
from schemas.search import SearchQuery, DishResponse
from schemas.order import CreateOrder
from schemas.feedback import CreateFeedback
from schemas.menu import DishCreate, UpdateDish
from services.orders import create_order, get_order, update_order_status, get_all_orders
from services.feedback import create_feedback, get_all_feedback
from services.dashboard import get_dashboard_kpis
from services.menu import create_dish, update_dish, delete_dish
from services.recommendations import get_recommendations
from pydantic import BaseModel
from typing import List, Optional
from config.db import get_dishes_collection

router = APIRouter(prefix="/api", tags=["spiceroute"])


# ─── SEARCH & INITIAL LOAD COMBINED ──────────────────────────────────────────

@router.get("/search", response_model=List[DishResponse])
def ai_search(
    query: str = Query("", description="Natural language search query"),
    max_price: float = Query(None, description="Max price filter"),
    category: str = Query(None, description="Category filter")
):
    """Unified route mapping database fields perfectly for the frontend layout grid"""
    dishes_collection = get_dishes_collection()
    
    clean_cat = None if (category and category.lower() == "all") else category

    # 1. Fetch raw documents
    if not query or query.strip() == "":
        db_query = {}
        if clean_cat:
            db_query["category"] = {"$regex": f"^{clean_cat.strip()}$", "$options": "i"}
        try:
            raw_results = list(dishes_collection.find(db_query))
        except Exception as e:
            print(f"❌ Direct DB Fetch Failed: {e}")
            raw_results = []
    else:
        try:
            raw_results = vector_search(query, max_price, clean_cat)
        except Exception as e:
            print(f"❌ Vector Search Failed: {e}")
            raw_results = []

    # 2. Map structural array items explicitly to match frontend key expectations
    formatted_dishes = []
    for r in raw_results:
        doc = r if isinstance(r, dict) else getattr(r, "__dict__", {})
        
        # Extract ID safely from _id, id, or dish_id string modifications
        db_id = str(doc.get("_id", doc.get("id", doc.get("dish_id", ""))))
        
        formatted_dishes.append(
            DishResponse(
                id=db_id,
                dish_id=db_id,                                      # Enforces frontend key rendering
                name=doc.get("name", "Unknown Dish"),
                description=doc.get("description", ""),
                price=float(doc.get("price", 0)),
                category=doc.get("category", "Mains"),
                dietary_tags=doc.get("dietary_tags", doc.get("tags", [])),
                tags=doc.get("dietary_tags", doc.get("tags", [])),   # Explicit duplicate property match
                is_available=doc.get("is_available", True),
                image_url=doc.get("image_url")
            )
        )
        
    return formatted_dishes
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


@router.get("/orders")
def list_orders():
    """Get all orders (for admin)"""
    return get_all_orders()


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

