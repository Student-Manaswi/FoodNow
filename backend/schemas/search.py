from pydantic import BaseModel
from typing import List, Optional

class DishResponse(BaseModel):
    id: str
    dish_id: str                      # Added to handle direct frontend card matching loops
    name: str
    description: str
    price: float
    category: str
    dietary_tags: List[str]
    tags: List[str] = []              # Added fallback array parameter property
    is_available: bool
    image_url: Optional[str] = None
    similarity_score: Optional[float] = None

class SearchQuery(BaseModel):
    query: str
    max_price: Optional[float] = None
    category: Optional[str] = None