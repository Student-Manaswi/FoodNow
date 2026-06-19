#!/usr/bin/env python3
"""
Seed the database with test users and admin accounts for development/testing
Run this once to populate test data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.auth import register_user, hash_password
from config.db import get_users_collection
from schemas.auth import UserRegister
from datetime import datetime, timezone
import uuid

def seed_test_users():
    """Create test users for development"""
    
    print("\n" + "=" * 60)
    print("🌱 SEEDING TEST USERS AND ADMIN")
    print("=" * 60)
    
    users_collection = get_users_collection()
    
    # Check if users already exist
    existing_count = users_collection.count_documents({})
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} user(s)")
        print("Skipping seed to avoid duplicates")
        return
    
    test_users = [
        {
            "name": "Customer One",
            "email": "customer1@example.com",
            "password": "Customer123!",
            "phone": "+91-9876543210",
            "role": "customer"
        },
        {
            "name": "Customer Two",
            "email": "customer2@example.com",
            "password": "Customer456!",
            "phone": "+91-9876543211",
            "role": "customer"
        },
        {
            "name": "Admin User",
            "email": "admin@foodnow.com",
            "password": "AdminPass123!",
            "phone": "+91-9999999999",
            "role": "admin"
        },
        {
            "name": "Test Kitchen",
            "email": "kitchen@foodnow.com",
            "password": "KitchenPass123!",
            "phone": "+91-8888888888",
            "role": "admin"
        }
    ]
    
    print("\nCreating test users:")
    print("-" * 60)
    
    for user_data in test_users:
        try:
            user_register = UserRegister(**user_data)
            user = register_user(user_register)
            print(f"✅ Created: {user['name']:20} ({user['email']})")
            print(f"   Role: {user['role']:10} | Phone: {user['phone']}")
        except ValueError as e:
            print(f"⚠️  {user_data['email']}: {str(e)}")
        except Exception as e:
            print(f"❌ Error creating {user_data['email']}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ USER SEEDING COMPLETE")
    print("=" * 60)
    
    print("\nTest Credentials for Login:")
    print("-" * 60)
    print("\nCustomer Account:")
    print('  Email:    customer1@example.com')
    print('  Password: Customer123!')
    print('  Role:     customer')
    print("\nAdmin Account:")
    print('  Email:    admin@foodnow.com')
    print('  Password: AdminPass123!')
    print('  Role:     admin')
    print("\n" + "=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        seed_test_users()
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
