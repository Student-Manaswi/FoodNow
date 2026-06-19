import os
import ssl
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import certifi
import ssl

backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=backend_dir / ".env")

MONGO_URI = os.getenv("MONGODB_URI")

# Attempt MongoDB Atlas connection with comprehensive TLS workarounds
client = None
db = None
using_mock = False

try:
    print("🔗 Attempting MongoDB Atlas connection...")
    # Use a consistent MongoClient configuration to bypass local TLS interception issues.
    # These options are safe for local development / network proxy workarounds only.
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    client = MongoClient(
        MONGO_URI,
        connectTimeoutMS=10000,
        serverSelectionTimeoutMS=10000,
        tls=True,
        tlsAllowInvalidCertificates=True,
        tlsAllowInvalidHostnames=True,
    )
    
    # Verify connection with a ping
    client.admin.command('ping')
    db = client["food_db"]
    print("✅ MongoDB Atlas connection successful!")
    
except Exception as e:
    print(f"⚠️  MongoDB Atlas connection failed: {str(e)[:100]}")
    print("📚 Falling back to MOCK DATABASE for local development...\n")
    
    # Fall back to mock database
    from config.mock_db import get_mock_db
    using_mock = True
    client, db = get_mock_db()

def get_dishes_collection():
    return db["dishes"]

def get_orders_collection():
    return db["orders"]

def get_users_collection():
    return db["users"]

def get_feedback_collection():
    return db["feedback"]

def is_mock_db():
    return using_mock
