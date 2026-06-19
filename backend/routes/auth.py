from fastapi import APIRouter, HTTPException
from schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from services.auth import register_user, login_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister):
    """Register new user"""
    try:
        user = register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user and return JWT token"""
    try:
        token_response = login_user(credentials.email, credentials.password)
        return token_response
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Login failed")