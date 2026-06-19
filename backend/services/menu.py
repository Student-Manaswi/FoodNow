from bson import ObjectId
from config.db import get_dishes_collection
from config.embeddings import get_embedding
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

dishes = get_dishes_collection()

def create_dish(name: str, description: str, category: str, price: float, tags: list) -> dict:
    text = f"{name} {description} {' '.join(tags)}"
    
    dish = {
        "name": name,
        "description": description,
        "category": category,
        "price": price,
        "dietary_tags": tags,
        "embedding": get_embedding(text),
        "is_available": True,
        "created_at": datetime.now(timezone.utc)
    }
    result = dishes.insert_one(dish)
    
    return {
        "id": str(result.inserted_id),
        "name": name,
        "description": description,
        "category": category,
        "price": price,
        "dietary_tags": tags,
        "is_available": True
    }

def update_dish(dish_id: str, data: dict) -> dict:
    dishes.update_one({"_id": ObjectId(dish_id)}, {"$set": data})
    dish = dishes.find_one({"_id": ObjectId(dish_id)})
    return {"id": str(dish["_id"]), "name": dish["name"], "price": dish["price"]}

def delete_dish(dish_id: str) -> bool:
    result = dishes.delete_one({"_id": ObjectId(dish_id)})
    return result.deleted_count > 0