from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from config.db import is_mock_db
import os

load_dotenv()

app = FastAPI(title="Food Ordering System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth routes (required)
from routes.auth import router as auth_router
app.include_router(auth_router)

# Include order routes (required)
from routes.orders import router as orders_router
app.include_router(orders_router)

# Include menu routes (required)
from routes.menu import router as menu_router
app.include_router(menu_router)

# Include search routes (optional - requires sentence_transformers)
try:
    from routes.search import router as search_router
    app.include_router(search_router)
    print("✅ Search routes loaded")
except ImportError as e:
    print(f"⚠️  Search routes skipped: {str(e)[:80]}")

@app.get("/api/health")
def health():
    db_status = "🔴 Mock DB (local dev)" if is_mock_db() else "🟢 MongoDB Atlas"
    return {
        "status": "✅ Backend live",
        "database": db_status
    }

@app.on_event("startup")
async def startup_event():
    db_type = "MOCK DATABASE" if is_mock_db() else "MongoDB Atlas"
    print(f"\n{'='*60}")
    print(f"🚀 Backend Started - Using: {db_type}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)