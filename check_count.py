import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"), tls=True, tlsAllowInvalidCertificates=True)
db = client["food_db"]
print("--- INSTANT DISH COUNT ---")
print("Dishes found:", db["dishes"].count_documents({}))
