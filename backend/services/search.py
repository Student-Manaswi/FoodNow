from config.db import get_dishes_collection
from config.embeddings import get_embedding
from schemas.search import DishResponse
from typing import List

dishes_collection = get_dishes_collection()

def vector_search(query: str, max_price: float = None, category: str = None) -> List[DishResponse]:
    """Hybrid semantic + structural search"""
    
    if not query:
        results = list(dishes_collection.find({"is_available": True}))
    else:
        query_embedding = get_embedding(query)
        
        # For MOCK DB: simple text matching
        results = list(dishes_collection.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"dietary_tags": {"$in": query.lower().split()}}
            ],
            "is_available": True
        }))
    
    if max_price:
        results = [r for r in results if r.get("price", 0) <= max_price]
    if category:
        results = [r for r in results if r.get("category") == category]
    
    return [
        DishResponse(
            id=str(r["_id"]),
            name=r["name"],
            description=r["description"],
            price=r["price"],
            category=r["category"],
            dietary_tags=r["dietary_tags"],
            is_available=r["is_available"],
            image_url=r.get("image_url")
        )
        for r in results
    ]