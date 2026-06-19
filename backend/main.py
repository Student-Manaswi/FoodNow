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
    # This runs BEFORE the server starts accepting incoming browser requests
    db_type = "MOCK DATABASE" if is_mock_db() else "MongoDB Atlas"
    print(f"\n{'='*60}")
    print(f"🚀 Backend Starting - Using: {db_type}")
    print(f"{'='*60}\n")
    
    # Safely look for and warm up the embedding model weights
    try:
        print("⏳ Pre-loading sentence-transformers model weights to prevent frontend timeouts...")
        from config.embeddings import get_embedding
        # Fire a quick fake query to initialize the torch tensors and model weights
        get_embedding("warmup")
        print("✅ Model weights loaded successfully. Server is primed and ready!")
    except ImportError:
        print("ℹ️ Skipping vector model warmup: config.embeddings not found or skipped.")
    except Exception as e:
        print(f"⚠️ Vector model warmup encountered an issue, skipping block: {e}")

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