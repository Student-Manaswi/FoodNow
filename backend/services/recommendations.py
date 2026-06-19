from config.db import get_dishes_collection

dishes_collection = get_dishes_collection()

def get_recommendations(cart_items: list) -> dict:
    """Get recommendation based on cart items"""
    
    all_tags = []
    for item in cart_items:
        all_tags.extend(item.get("dietary_tags", []))
    
    print(f"DEBUG: Cart tags = {all_tags}")  # Debug
    
    # Check for spicy
    if "spicy" in all_tags:
        cooling = dishes_collection.find_one({
            "category": {"$in": ["Beverages", "Desserts"]},
            "dietary_tags": "cooling"  # Single tag as string
        })
        print(f"DEBUG: Found cooling dish = {cooling}")  # Debug
        if cooling:
            return {
                "recommendation_text": f"Pair with {cooling['name']} to cool down the heat!",
                "dish_id": str(cooling["_id"]),
                "dish_name": cooling["name"],
                "price": cooling["price"]
            }
    
    return {"recommendation_text": "No recommendation available"}