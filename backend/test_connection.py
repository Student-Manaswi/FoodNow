import os
from pymongo import MongoClient
from dotenv import load_dotenv
import ssl

load_dotenv()

print("="*70)
print("MongoDB Atlas Connection Test")
print("="*70)
print("\n🔧 Testing MongoDB Atlas connectivity with comprehensive TLS workarounds...")
print("💡 NOTE: Backend auto-falls back to MOCK DATABASE if Atlas fails!")
print("   This script helps identify which TLS strategy works in your environment.\n")

# Try multiple connection strategies
strategies = [
    {
        "name": "Strategy 1: Full TLS Bypass (tlsInsecure=True)",
        "kwargs": {
            "tls": True,
            "tlsInsecure": True,
            "connectTimeoutMS": 10000,
            "serverSelectionTimeoutMS": 10000,
        }
    },
    {
        "name": "Strategy 2: TLS + Invalid Certs + Hostnames",
        "kwargs": {
            "tls": True,
            "tlsAllowInvalidCertificates": True,
            "tlsAllowInvalidHostnames": True,
            "connectTimeoutMS": 10000,
            "serverSelectionTimeoutMS": 10000,
        }
    },
    {
        "name": "Strategy 3: No TLS (direct TCP)",
        "kwargs": {
            "tls": False,
            "connectTimeoutMS": 10000,
            "serverSelectionTimeoutMS": 10000,
        }
    },
    {
        "name": "Strategy 4: TLS with SSL defaults + IPv4 only",
        "kwargs": {
            "tls": True,
            "tlsAllowInvalidCertificates": True,
            "connectTimeoutMS": 15000,
            "serverSelectionTimeoutMS": 15000,
            "ipv6": False,
            "retryWrites": False,
        }
    },
]

mongo_uri = os.getenv("MONGODB_URI")
connected = False

for strategy in strategies:
    try:
        print(f"⏳ {strategy['name']}...")
        client = MongoClient(mongo_uri, **strategy["kwargs"])
        
        # Try a ping to verify connection
        client.admin.command('ping')
        db = client["food_db"]
        count = db["dishes"].count_documents({})
        
        print(f"✅ SUCCESS: {strategy['name']}")
        print(f"📊 Dishes found: {count}\n")
        connected = True
        break
        
    except Exception as e:
        error_msg = str(e)[:150]  # Truncate for readability
        print(f"❌ Failed: {error_msg}\n")
        continue

if not connected:
    print("⚠️  All Atlas strategies failed. Using LOCAL MOCK DATABASE for development.\n")
    print("📝 Switch to a different network or configure a local MongoDB instance.")

