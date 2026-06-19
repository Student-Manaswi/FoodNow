from pydantic import BaseModel

class CreateFeedback(BaseModel):
    order_id: str
    rating: int  # 1-5
    comment: str