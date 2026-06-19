from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
model = SentenceTransformer('all-MiniLM-L6-v2')

dishes = [
    # Appetizers
    {"name": "Paneer Tikka", "description": "Grilled cottage cheese marinated in spiced yogurt", "category": "Appetizers", "price": 250, "dietary_tags": ["vegetarian", "spicy"]},
    {"name": "Samosa", "description": "Crispy fried pastry with potato filling", "category": "Appetizers", "price": 80, "dietary_tags": ["vegetarian", "spicy"]},
    {"name": "Spring Rolls", "description": "Crispy rolls with cabbage and carrots", "category": "Appetizers", "price": 120, "dietary_tags": ["vegetarian", "light"]},
    {"name": "Chicken Tikka", "description": "Grilled chicken marinated in yogurt and spices", "category": "Appetizers", "price": 280, "dietary_tags": ["non-vegetarian", "spicy"]},
    {"name": "Pakora", "description": "Crispy vegetable fritters", "category": "Appetizers", "price": 100, "dietary_tags": ["vegetarian", "spicy"]},
    {"name": "Garlic Bread", "description": "Toasted bread with garlic butter", "category": "Appetizers", "price": 90, "dietary_tags": ["vegetarian"]},
    
    # Mains - Vegetarian
    {"name": "Paneer Butter Masala", "description": "Cottage cheese in creamy tomato gravy", "category": "Mains", "price": 280, "dietary_tags": ["vegetarian", "creamy", "heavy"]},
    {"name": "Dal Makhani", "description": "Black lentils in buttery tomato sauce", "category": "Mains", "price": 200, "dietary_tags": ["vegetarian", "heavy"]},
    {"name": "Aloo Gobi", "description": "Potato and cauliflower curry", "category": "Mains", "price": 150, "dietary_tags": ["vegetarian", "light"]},
    {"name": "Palak Paneer", "description": "Cottage cheese in spinach gravy", "category": "Mains", "price": 220, "dietary_tags": ["vegetarian", "healthy"]},
    {"name": "Chana Masala", "description": "Chickpea curry with tomato sauce", "category": "Mains", "price": 140, "dietary_tags": ["vegetarian", "vegan"]},
    {"name": "Vegetable Biryani", "description": "Fragrant rice with mixed vegetables", "category": "Mains", "price": 180, "dietary_tags": ["vegetarian", "light"]},
    
    # Mains - Non-Vegetarian
    {"name": "Butter Chicken", "description": "Tender chicken in creamy tomato sauce", "category": "Mains", "price": 320, "dietary_tags": ["non-vegetarian", "creamy"]},
    {"name": "Chicken Tikka Masala", "description": "Grilled chicken in spiced cream sauce", "category": "Mains", "price": 300, "dietary_tags": ["non-vegetarian", "spicy"]},
    {"name": "Chicken Biryani", "description": "Fragrant rice with tender chicken", "category": "Mains", "price": 280, "dietary_tags": ["non-vegetarian", "heavy"]},
    {"name": "Rogan Josh", "description": "Lamb in aromatic spice blend", "category": "Mains", "price": 350, "dietary_tags": ["non-vegetarian", "spicy"]},
    {"name": "Fish Curry", "description": "Fresh fish in coconut gravy", "category": "Mains", "price": 320, "dietary_tags": ["non-vegetarian", "light", "healthy"]},
    {"name": "Tandoori Chicken", "description": "Grilled chicken with tandoori spices", "category": "Mains", "price": 280, "dietary_tags": ["non-vegetarian", "spicy", "healthy"]},
    {"name": "Shrimp Masala", "description": "Shrimp in spiced tomato sauce", "category": "Mains", "price": 380, "dietary_tags": ["non-vegetarian", "spicy"]},
    {"name": "Chettinad Chicken", "description": "Spicy chicken with regional spices", "category": "Mains", "price": 300, "dietary_tags": ["non-vegetarian", "spicy", "heavy"]},
    
    # Rice & Noodles
    {"name": "Vegetable Fried Rice", "description": "Stir-fried rice with mixed vegetables", "category": "Rice & Noodles", "price": 150, "dietary_tags": ["vegetarian", "light"]},
    {"name": "Egg Fried Rice", "description": "Fried rice with scrambled eggs", "category": "Rice & Noodles", "price": 170, "dietary_tags": ["non-vegetarian", "light"]},
    {"name": "Chicken Fried Rice", "description": "Fried rice with chicken pieces", "category": "Rice & Noodles", "price": 200, "dietary_tags": ["non-vegetarian", "light"]},
    {"name": "Hakka Noodles", "description": "Stir-fried noodles with vegetables", "category": "Rice & Noodles", "price": 140, "dietary_tags": ["vegetarian", "light"]},
    {"name": "Chow Mein", "description": "Crispy noodles with sauce", "category": "Rice & Noodles", "price": 160, "dietary_tags": ["vegetarian", "light"]},
    
    # Breads
    {"name": "Naan", "description": "Soft Indian bread from clay oven", "category": "Breads", "price": 60, "dietary_tags": ["vegetarian"]},
    {"name": "Roti", "description": "Thin whole wheat bread", "category": "Breads", "price": 40, "dietary_tags": ["vegetarian", "healthy"]},
    {"name": "Paratha", "description": "Layered buttered bread", "category": "Breads", "price": 80, "dietary_tags": ["vegetarian", "heavy"]},
    {"name": "Puri", "description": "Fried Indian bread", "category": "Breads", "price": 50, "dietary_tags": ["vegetarian"]},
    {"name": "Garlic Naan", "description": "Naan with garlic and herbs", "category": "Breads", "price": 80, "dietary_tags": ["vegetarian"]},
    
    # Desserts
    {"name": "Gulab Jamun", "description": "Soft milk dumplings in sugar syrup", "category": "Desserts", "price": 120, "dietary_tags": ["vegetarian", "sweet"]},
    {"name": "Kheer", "description": "Rice pudding with condensed milk", "category": "Desserts", "price": 100, "dietary_tags": ["vegetarian", "sweet"]},
    {"name": "Laddu", "description": "Sweet round balls made from gram flour", "category": "Desserts", "price": 150, "dietary_tags": ["vegetarian", "sweet"]},
    {"name": "Jalebi", "description": "Spiral sweet soaked in sugar syrup", "category": "Desserts", "price": 80, "dietary_tags": ["vegetarian", "sweet"]},
    {"name": "Chocolate Lava Cake", "description": "Warm chocolate cake with molten center", "category": "Desserts", "price": 180, "dietary_tags": ["vegetarian", "sweet"]},
    {"name": "Mango Cheesecake", "description": "Creamy cheesecake with mango puree", "category": "Desserts", "price": 200, "dietary_tags": ["vegetarian", "sweet"]},
    
    # Beverages
    {"name": "Mango Lassi", "description": "Chilled yogurt drink with mango", "category": "Beverages", "price": 80, "dietary_tags": ["vegetarian", "cooling", "sweet"]},
    {"name": "Masala Chai", "description": "Spiced Indian tea with milk", "category": "Beverages", "price": 50, "dietary_tags": ["vegetarian", "hot"]},
    {"name": "Fresh Lime Soda", "description": "Sparkling water with lime and salt", "category": "Beverages", "price": 60, "dietary_tags": ["vegetarian", "cooling"]},
    {"name": "Iced Coffee", "description": "Cold coffee with milk and cream", "category": "Beverages", "price": 100, "dietary_tags": ["vegetarian", "cold"]},
    {"name": "Mango Juice", "description": "Fresh mango juice", "category": "Beverages", "price": 70, "dietary_tags": ["vegetarian", "vegan", "healthy"]},
    {"name": "Strawberry Smoothie", "description": "Blended strawberries with yogurt", "category": "Beverages", "price": 120, "dietary_tags": ["vegetarian", "healthy"]},
    {"name": "Watermelon Juice", "description": "Fresh watermelon juice", "category": "Beverages", "price": 80, "dietary_tags": ["vegetarian", "vegan", "cooling"]},
    
    # Soups
    {"name": "Tomato Soup", "description": "Creamy tomato soup", "category": "Soups", "price": 100, "dietary_tags": ["vegetarian", "light"]},
    {"name": "Mushroom Soup", "description": "Creamy mushroom soup with herbs", "category": "Soups", "price": 120, "dietary_tags": ["vegetarian", "light"]},
    {"name": "Chicken Soup", "description": "Light broth with chicken pieces", "category": "Soups", "price": 130, "dietary_tags": ["non-vegetarian", "light"]},
]

# Generate embeddings
texts = [f"{d['name']}. {d['description']}. Tags: {', '.join(d['dietary_tags'])}" for d in dishes]
embeddings = model.encode(texts, show_progress_bar=True)

for i, dish in enumerate(dishes):
    dish['embedding'] = embeddings[i].tolist()
    dish['is_available'] = True
    dish['created_at'] = datetime.now(timezone.utc)

# Connect and seed
client = MongoClient(MONGO_URI)
db = client['food_db']
collection = db['dishes']

# Clear existing and insert
collection.delete_many({})
result = collection.insert_many(dishes)

print(f"✅ Inserted {len(result.inserted_ids)} dishes with embeddings to MongoDB Atlas")
client.close()