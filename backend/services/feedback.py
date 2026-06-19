from config.db import get_feedback_collection
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

feedback_collection = get_feedback_collection()

def serialize_feedback(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    if isinstance(doc.get("created_at"), datetime):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc

def create_feedback(order_id: str, rating: int, comment: str) -> dict:
    feedback = {
        "order_id": order_id,
        "rating": rating,
        "comment": comment,
        "photo_urls": [],
        "created_at": datetime.now(timezone.utc)
    }
    result = feedback_collection.insert_one(feedback)
    feedback["id"] = str(result.inserted_id)
    del feedback["_id"]
    feedback["created_at"] = feedback["created_at"].isoformat()
    return feedback

def get_all_feedback() -> list:
    docs = list(feedback_collection.find().sort("created_at", -1))
    return [serialize_feedback(doc) for doc in docs]