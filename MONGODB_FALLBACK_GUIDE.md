# MongoDB Fallback System Guide

## Overview

The FoodNow backend now includes **automatic graceful fallback** to a mock in-memory database if MongoDB Atlas connection fails. This allows you to develop, test, and demonstrate the entire application locally without internet connectivity or network configuration issues.

## How It Works

### 1. **Connection Priority**

- **Primary**: MongoDB Atlas (production-grade cloud database)
- **Fallback**: Mock Database (local in-memory storage)

### 2. **Backend Startup Flow**

When you start the backend:

```bash
python -m uvicorn main:app --reload
```

The system attempts to:

1. **Connect to MongoDB Atlas** with comprehensive TLS bypass options
2. **Verify connection** with a ping command
3. **If successful** → Uses Atlas (message: "✅ MongoDB Atlas connection successful!")
4. **If failed** → Falls back to mock DB (message: "📚 Falling back to MOCK DATABASE for local development...")

### 3. **Database Status Indicators**

Check which database is being used:

```bash
# Health check endpoint
curl http://localhost:8000/api/health
```

Response examples:

```json
# Using MongoDB Atlas
{
  "status": "✅ Backend live",
  "database": "🟢 MongoDB Atlas"
}

# Using Mock Database
{
  "status": "✅ Backend live",
  "database": "🔴 Mock DB (local dev)"
}
```

Startup banner also shows:

```
============================================================
🚀 Backend Started - Using: MongoDB Atlas
============================================================
```

Or:

```
============================================================
🚀 Backend Started - Using: MOCK DATABASE
============================================================
```

## When to Use Each Database

### ✅ Use Mock Database When:

- **Developing locally** without internet access
- **Network has TLS interception** (corporate firewall, ISP proxy)
- **MongoDB Atlas is unreachable** for any reason
- **Testing API routes** without needing persistent data
- **Running continuous integration** without cloud dependencies

### ✅ Use MongoDB Atlas When:

- **Production deployment** (required)
- **Need persistent data** across sessions
- **Integrating with other services** expecting real database
- **Network allows direct HTTPS connections** to MongoDB

## Mock Database Features

The mock database (`config/mock_db.py`) provides:

### Collections

- `dishes` - Menu items
- `orders` - Customer orders
- `feedback` - Customer feedback

### Pre-Seeded Sample Data

5 sample dishes are automatically loaded:

1. Butter Chicken (280₹)
2. Vegetable Fried Rice (150₹)
3. Mango Lassi (80₹)
4. Tandoori Paneer (180₹)
5. Gulab Jamun (120₹)

### Supported Operations

```python
collection.insert_one(doc)      # Add document
collection.find_one(query)      # Find single document
collection.find(query)          # Find multiple documents
collection.count_documents()    # Count matching documents
collection.update_one(query, update)  # Update document
collection.delete_one(query)    # Delete document
collection.aggregate(pipeline)  # Run aggregation pipeline
```

### Data Persistence

**Important**: Mock database data is **NOT persistent**. Each server restart clears all data and reloads sample data.

For development scenarios:

- Use for testing API endpoints
- Use for frontend development
- Use for demonstrations
- **Don't use for testing data persistence**

## Testing MongoDB Atlas Connectivity

Run the connection test script:

```bash
cd backend
python test_connection.py
```

This tests 4 different TLS strategies:

1. Full TLS Bypass (`tlsInsecure=True`)
2. TLS + Invalid Certs + Invalid Hostnames
3. No TLS (direct TCP)
4. TLS with IPv4 only + custom settings

Output shows which strategy succeeds:

```
⏳ Strategy 1: Full TLS Bypass (tlsInsecure=True)...
✅ SUCCESS: Strategy 1: Full TLS Bypass (tlsInsecure=True)
📊 Dishes found: 47
```

## Transitioning from Mock to MongoDB Atlas

Once Atlas connectivity is working:

1. **Verify connection** with `python test_connection.py`
2. **Restart backend** - it will automatically connect to Atlas
3. **Check health endpoint** - should show "🟢 MongoDB Atlas"
4. **Test API routes** - all existing routes work unchanged

No code changes needed! The same routes work with either database.

## Switching Between Databases (For Testing)

### Force Mock Database (Development)

Edit `config/db.py` and comment out the try block:

```python
# Temporarily force mock DB for testing
# try:
#     ... (MongoDB code)
# except:
#     pass

from config.mock_db import get_mock_db
using_mock = True
client, db = get_mock_db()
```

### Force MongoDB Atlas

Comment out the mock DB fallback and ensure MONGODB_URI is correct:

```python
# .env file
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

## Troubleshooting

### Problem: "All strategies failed. Using MOCK DATABASE"

**Cause**: Cannot reach MongoDB Atlas

**Solutions**:

1. Check `.env` has valid `MONGODB_URI`
2. Run `python test_connection.py` to identify which TLS strategy would work
3. Try from different network (mobile hotspot, VPN)
4. Temporarily use mock DB (automatically enabled)

### Problem: "Connection successful but no data"

**Cause**: Atlas connected but database is empty

**Solutions**:

1. Run seed script: `python seed_dishes.py`
2. Verify cluster has data in MongoDB Atlas console
3. Check database name is "food_db"

### Problem: Frontend shows "API error"

**Cause**: Backend using mock DB without data

**Solutions**:

1. Mock DB auto-seeds 5 dishes - should be visible
2. Restart backend to reload seed data
3. Check `/api/health` to see which DB is active

## Architecture Details

### File Structure

```
backend/
├── config/
│   ├── db.py              # Connection logic with fallback
│   └── mock_db.py         # Mock database implementation (NEW)
├── main.py                # FastAPI app with startup event
├── test_connection.py     # Atlas connectivity tester
└── ...
```

### Connection Flow

```
Request to Backend
    ↓
config.db.py loads
    ↓
Try MongoDB Atlas connection
    ├─ Success → Use Atlas
    └─ Failure → Fall back to Mock DB
    ↓
api/health endpoint shows which is active
    ↓
All routes work identically
```

### Code Examples

**Checking active database in routes:**

```python
from config.db import is_mock_db, get_dishes_collection

@app.get("/api/dishes")
def get_dishes():
    if is_mock_db():
        print("Using mock database - data not persistent")

    dishes = get_dishes_collection().find()
    return dishes
```

## Performance Notes

### Mock Database

- **Speed**: Extremely fast (in-memory)
- **Scalability**: Limited to available RAM
- **Features**: Basic operations only
- **Use case**: Development & testing

### MongoDB Atlas

- **Speed**: Network latency (typically 50-200ms)
- **Scalability**: Virtually unlimited
- **Features**: Full MongoDB capabilities (aggregation, indexing, etc.)
- **Use case**: Production

## Summary

| Aspect           | Mock DB                | MongoDB Atlas              |
| ---------------- | ---------------------- | -------------------------- |
| Setup            | Zero setup             | Requires connection string |
| Speed            | Instant                | Network dependent          |
| Data persistence | No (clears on restart) | Yes (permanent)            |
| Use case         | Development            | Production                 |
| Fallback         | N/A                    | Primary                    |

Start developing with whatever database is available, and switch to Atlas when ready for production!
