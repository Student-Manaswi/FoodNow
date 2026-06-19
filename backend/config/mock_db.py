# Mock in-memory database for local development when MongoDB Atlas is unreachable
# This allows full frontend testing without network connectivity

from datetime import datetime, timezone
from bson import ObjectId
from typing import List, Dict, Any

class MockCollection:
    def __init__(self, name: str):
        self.name = name
        self.data: Dict[str, Any] = {}
        self._counter = 0
    
    def insert_one(self, doc: Dict) -> object:
        doc_id = ObjectId()
        doc["_id"] = doc_id
        self.data[str(doc_id)] = doc
        self._counter += 1
        
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        
        return InsertResult(doc_id)
    
    def find(self, query: Dict = None):
        if not query:
            results = list(self.data.values())
        else:
            results = []
            for doc in self.data.values():
                match = True
                for key, value in query.items():
                    if key not in doc:
                        match = False
                        break
                    if isinstance(value, dict):
                        if "$in" in value and doc[key] not in value["$in"]:
                            match = False
                        elif "$gte" in value and doc[key] < value["$gte"]:
                            match = False
                        elif "$lte" in value and doc[key] > value["$lte"]:
                            match = False
                    elif doc[key] != value:
                        match = False
                        break
                if match:
                    results.append(doc)
        return MockCursor(results)


class MockCursor:
    def __init__(self, results):
        self.results = results

    def sort(self, key, direction=1):
        self.results = sorted(self.results, key=lambda d: d.get(key, 0), reverse=(direction == -1))
        return self

    def __iter__(self):
        return iter(self.results)

    def __list__(self):
        return list(self.results)
    
    def find_one(self, query: Dict = None) -> Dict:
        results = self.find(query)
        return results[0] if results else None
    
    def update_one(self, query: Dict, update: Dict) -> object:
        doc = self.find_one(query)
        if doc:
            if "$set" in update:
                doc.update(update["$set"])
            else:
                doc.update(update)
        
        class UpdateResult:
            def __init__(self, matched=0):
                self.matched_count = matched
        
        return UpdateResult(1 if doc else 0)
    
    def delete_one(self, query: Dict) -> object:
        doc = self.find_one(query)
        deleted = 0
        if doc:
            del self.data[str(doc["_id"])]
            deleted = 1
        
        class DeleteResult:
            def __init__(self, count=0):
                self.deleted_count = count
        
        return DeleteResult(deleted)
    
    def count_documents(self, query: Dict = None) -> int:
        return len(self.find(query))
    
    def aggregate(self, pipeline: List[Dict]) -> List[Dict]:
        # Simplified aggregation - just return all docs for now
        return list(self.data.values())
    
    def sort(self, key_or_list, direction=1):
        return list(self.data.values())

class MockDB:
    def __init__(self):
        self.collections: Dict[str, MockCollection] = {}
    
    def __getitem__(self, collection_name: str) -> MockCollection:
        if collection_name not in self.collections:
            self.collections[collection_name] = MockCollection(collection_name)
        return self.collections[collection_name]
    
    def close(self):
        pass

class MockMongoClient:
    def __init__(self, *args, **kwargs):
        self.db = MockDB()
        print("⚠️  Using MOCK DATABASE (in-memory storage for development only)")
    
    def __getitem__(self, db_name: str) -> MockDB:
        return self.db
    
    def close(self):
        self.db.close()

# Seed mock data on import
def get_mock_db():
    client = MockMongoClient()
    mock_db = client["food_db"]
    
    # Seed dishes
    dishes = [
        {"name": "Butter Chicken", "description": "Creamy tomato sauce", "category": "Mains", "price": 280, "dietary_tags": ["non-veg", "spicy", "creamy"], "is_available": True, "embedding": []},
        {"name": "Vegetable Fried Rice", "description": "Light fluffy rice", "category": "Mains", "price": 150, "dietary_tags": ["veg", "light"], "is_available": True, "embedding": []},
        {"name": "Mango Lassi", "description": "Cooling yogurt drink", "category": "Beverages", "price": 80, "dietary_tags": ["veg", "cooling"], "is_available": True, "embedding": []},
        {"name": "Tandoori Paneer", "description": "Grilled cottage cheese", "category": "Appetizers", "price": 180, "dietary_tags": ["veg", "spicy"], "is_available": True, "embedding": []},
        {"name": "Gulab Jamun", "description": "Sweet milk dumplings", "category": "Desserts", "price": 120, "dietary_tags": ["veg", "sweet"], "is_available": True, "embedding": []},
    ]
    
    dishes_col = mock_db["dishes"]
    for dish in dishes:
        dishes_col.insert_one(dish)
    
    print(f"✅ Mock DB seeded with {len(dishes)} sample dishes")
    return client, mock_db
