from pydantic import BaseModel, Field
from typing import List, Optional

class DishBase(BaseModel):
    name: str = Field(..., example="Paneer Tikka")
    description: str = Field(..., example="Spicy grilled cottage cheese cooked with peppers")
    category: str = Field(..., example="Appetizers") # Appetizers, Mains, Desserts, Beverages
    price: float = Field(..., gt=0, example=180.0)
    dietary_tags: List[str] = Field(default=[], example=["vegetarian", "spicy"])
    is_available: bool = True

class DishCreate(DishBase):
    pass

class DishResponse(DishBase):
    id: str

class CartItemInput(BaseModel):
    menu_id: str
    name: str
    tags: List[str]

class UpdateDish(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None