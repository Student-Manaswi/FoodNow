from config.db import get_dishes_collection
from config.embeddings import get_embedding
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

dishes_collection = get_dishes_collection()

sample_dishes = [
    {"name": "Butter Chicken", "description": "Creamy tomato sauce", "category": "Mains", "price": 280, "dietary_tags": ["non-veg", "spicy", "creamy"]},
    {"name": "Vegetable Fried Rice", "description": "Light fluffy rice", "category": "Mains", "price": 150, "dietary_tags": ["veg", "light"]},
    {"name": "Mango Lassi", "description": "Cooling yogurt drink", "category": "Beverages", "price": 80, "dietary_tags": ["veg", "cooling"]},
    {"name": "Tandoori Paneer", "description": "Grilled cottage cheese", "category": "Appetizers", "price": 180, "dietary_tags": ["veg", "spicy"]},
    {"name": "Gulab Jamun", "description": "Sweet milk dumplings", "category": "Desserts", "price": 120, "dietary_tags": ["veg", "sweet"]},
]

print("⏳ Seeding dishes with embeddings...\n")

for dish in sample_dishes:
    embedding_text = f"{dish['name']} {dish['description']} {' '.join(dish['dietary_tags'])}"
    dish['embedding'] = get_embedding(embedding_text)
    dish['is_available'] = True
    dish['created_at'] = datetime.utcnow()
    
    dishes_collection.update_one(
        {"name": dish["name"]},
        {"$set": dish},
        upsert=True
    )
    print(f"✅ {dish['name']} - ₹{dish['price']}")

print(f"\n✅ {len(sample_dishes)} dishes seeded!")