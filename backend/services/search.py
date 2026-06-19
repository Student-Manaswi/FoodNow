from config.db import get_dishes_collection
from config.embeddings import get_embedding
from schemas.search import DishResponse
from typing import List

dishes_collection = get_dishes_collection()

def vector_search(query: str, max_price: float = None, category: str = None) -> List[DishResponse]:
    """Hybrid semantic + structural search using MongoDB Atlas Vector Search"""
    
    # Standardize string checking for universal 'all' tags
    clean_cat = None if (category and category.lower() == "all") else category

    if not query or query.strip() == "":
        db_query = {"is_available": True}
        if clean_cat:
            db_query["category"] = {"$regex": f"^{clean_cat.strip()}$", "$options": "i"}
        results = list(dishes_collection.find(db_query))
    else:
        query_embedding = get_embedding(query)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "menu_vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": 20
                }
            },
            {
                "$addFields": {
                    "similarityScore": {"$meta": "searchScore"}
                }
            },
            {
                "$match": {
                    "is_available": True
                }
            }
        ]
        
        if max_price:
            pipeline.append({"$match": {"price": {"$lte": max_price}}})
        
        if clean_cat:
            pipeline.append({"$match": {"category": {"$regex": f"^{clean_cat.strip()}$", "$options": "i"}}})
        
        try:
            results = list(dishes_collection.aggregate(pipeline))
        except Exception as e:
            print(f"Vector search failed: {e}. Falling back to text matching.")
            results = list(dishes_collection.find({
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}}
                ],
                "is_available": True
            }))
            
    return [
        DishResponse(
            id=str(r["_id"]),
            dish_id=str(r["_id"]),
            name=r["name"],
            description=r["description"],
            price=float(r["price"]),
            category=r["category"],
            dietary_tags=r.get("dietary_tags", []),
            tags=r.get("dietary_tags", []),
            is_available=r.get("is_available", True),
            image_url=r.get("image_url"),
            similarity_score=r.get("similarityScore")
        )
        for r in results
    ]