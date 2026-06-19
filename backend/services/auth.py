from config.db import get_users_collection
from schemas.auth import UserRegister, UserResponse
from middleware.jwt import create_access_token
from datetime import datetime, timezone
import bcrypt
import uuid

users_collection = get_users_collection()

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def register_user(user_data: UserRegister) -> dict:
    """Register new user"""
    # Check if user already exists
    existing_user = users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise ValueError("Email already registered")
    
    # Create user document
    user = {
        "user_id": str(uuid.uuid4()),
        "name": user_data.name,
        "email": user_data.email,
        "phone": user_data.phone,
        "password_hash": hash_password(user_data.password),
        "role": user_data.role,
        "created_at": datetime.now(timezone.utc)
    }
    
    result = users_collection.insert_one(user)
    user["_id"] = str(result.inserted_id)
    
    return serialize_user(user)

def login_user(email: str, password: str) -> dict:
    """Authenticate user and return token"""
    user = users_collection.find_one({"email": email})
    
    if not user or not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid email or password")
    
    # Create token
    token_data = {
        "sub": user["user_id"],
        "role": user["role"],
        "email": user["email"]
    }
    
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"],
        "user_id": user["user_id"]
    }

def get_user_by_id(user_id: str) -> dict:
    """Get user by user_id"""
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        raise ValueError("User not found")
    return serialize_user(user)

def serialize_user(user: dict) -> dict:
    """Convert MongoDB user document to response format"""
    return {
        "id": user.get("user_id"),
        "name": user.get("name"),
        "email": user.get("email"),
        "phone": user.get("phone"),
        "role": user.get("role"),
        "created_at": user.get("created_at")
    }
