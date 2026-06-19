#!/usr/bin/env python3
"""
Verify that all authentication system dependencies are installed correctly
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    packages = {
        'fastapi': 'FastAPI framework',
        'pydantic': 'Data validation',
        'pymongo': 'MongoDB driver',
        'jwt': 'PyJWT - JWT token handling',
        'bcrypt': 'Password hashing',
        'jose': 'Python-JOSE - JOSE library',
        'email_validator': 'Email validation',
        'cryptography': 'Cryptographic operations'
    }
    
    print("=" * 60)
    print("🔍 VERIFYING AUTHENTICATION SYSTEM DEPENDENCIES")
    print("=" * 60)
    
    failed = []
    
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✅ {package:20} - {description}")
        except ImportError as e:
            print(f"❌ {package:20} - {description}")
            failed.append((package, str(e)))
    
    print("\n" + "=" * 60)
    
    if failed:
        print(f"⚠️  {len(failed)} package(s) missing!")
        print("\nInstall missing packages with:")
        print("python -m pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed successfully!")
        return True

def test_auth_module():
    """Test if auth modules can be imported"""
    print("\n" + "=" * 60)
    print("🔐 TESTING AUTH MODULE IMPORTS")
    print("=" * 60)
    
    try:
        from schemas.auth import UserRegister, UserLogin, TokenResponse
        print("✅ Auth schemas imported successfully")
        
        from middleware.jwt import create_access_token, get_current_user
        print("✅ JWT middleware imported successfully")
        
        from services.auth import register_user, login_user, hash_password
        print("✅ Auth services imported successfully")
        
        from routes.auth import router as auth_router
        print("✅ Auth routes imported successfully")
        
        from services.orders import create_order, get_user_orders
        print("✅ Order services updated successfully")
        
        from routes.orders import router as orders_router
        print("✅ Order routes created successfully")
        
        print("\n✅ All auth modules imported successfully!")
        return True
    
    except Exception as e:
        print(f"❌ Error importing auth modules: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n" + "=" * 60)
    print("🗄️  TESTING DATABASE CONNECTION")
    print("=" * 60)
    
    try:
        from config.db import get_users_collection, is_mock_db
        print("✅ Database config imported successfully")
        
        users_col = get_users_collection()
        print(f"✅ Users collection accessible")
        
        if is_mock_db():
            print("⚠️  Using MOCK DATABASE (development mode)")
            print("   To use MongoDB Atlas, update MONGODB_URI in .env")
        else:
            print("✅ Connected to MongoDB Atlas")
        
        return True
    
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Run all verification tests"""
    
    print("\n")
    
    # Test 1: Package imports
    result1 = test_imports()
    
    # Test 2: Auth modules
    result2 = test_auth_module() if result1 else False
    
    # Test 3: Database
    result3 = test_database() if result2 else False
    
    print("\n" + "=" * 60)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 60)
    
    if result1 and result2 and result3:
        print("✅ ✅ ✅ ALL SYSTEMS READY FOR AUTHENTICATION!")
        print("\nYou can now:")
        print("  1. Start backend: python main.py")
        print("  2. Test endpoints: Use test_auth_orders.http file")
        print("  3. Update frontend with auth service")
        print("\n" + "=" * 60)
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nNext steps:")
        print("  1. Check error messages above")
        print("  2. Run: python -m pip install -r requirements.txt")
        print("  3. Verify .env file has JWT_SECRET_KEY")
        print("  4. Check that backend/.env exists")
        print("\n" + "=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
