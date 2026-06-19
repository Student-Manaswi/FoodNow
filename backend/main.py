from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from config.db import is_mock_db
import os

load_dotenv()

# ─── LIFESPAN EVENT HANDLER (FOR WARMING UP MODELS) ───────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    db_type = "MOCK DATABASE" if is_mock_db() else "MongoDB Atlas"
    print(f"\n🚀 Backend Starting - Using: {db_type}")
    
    # Fast network handshake test
    try:
        print("⏳ Testing serverless Hugging Face API connection...")
        from config.embeddings import get_embedding
        get_embedding("warmup")
        print("✅ Cloud Inference token verified successfully!")
    except Exception as e:
        print(f"⚠️ Pre-warmup skipped or delayed: {e}")

    yield
    # Any teardown or cleanup actions go here on server close

# Pass the unified lifespan context into the FastAPI instance
app = FastAPI(title="Food Ordering System API", lifespan=lifespan)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)