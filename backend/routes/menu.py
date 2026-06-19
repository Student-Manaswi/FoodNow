from fastapi import APIRouter, HTTPException, status
from config.db import get_dishes_collection
from schemas.menu import DishCreate, DishResponse
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/api/dishes", tags=["Menu Management"])

@router.get("/", response_model=List[DishResponse])
def get_all_dishes():
    """Fetches all menu items from the database."""
    collection = get_dishes_collection()
    dishes = []
    for doc in collection.find():
        doc["id"] = str(doc["_id"]) # Convert MongoDB ObjectId to readable string id
        dishes.append(doc)
    return dishes

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_dish(dish: DishCreate):
    """Admin endpoint to add a new dish directly to the menu."""
    collection = get_dishes_collection()
    
    # Check if a dish with the same name already exists
    if collection.find_one({"name": dish.name}):
        raise HTTPException(status_code=400, detail="A dish with this name already exists!")
        
    dish_dict = dish.model_dump()
    # Note: Tomorrow we will inject the AI vector array here before saving!
    dish_dict["embedding"] = [] 
    
    result = collection.insert_one(dish_dict)
    return {"status": "success", "inserted_id": str(result.inserted_id)}
