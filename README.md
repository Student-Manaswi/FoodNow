```markdown
# 🌶️ FoodNow - Full-Stack AI Food Ordering System

FoodNow is a modern, full-stack food ordering platform designed with an AI-powered semantic menu search engine and a smart cross-sell cart recommendation companion. Instead of relying on strict keyword matching, customers can search for dishes using natural language phrases like *"something light and vegetarian for dinner"* or *"spicy noodles with chicken"*, while getting real-time structural pairing recommendations based on their current cart state.

The platform utilizes **FastAPI**, **MongoDB Atlas Vector Search**, and a rule/LLM hybrid recommendation context, alongside a fast **React (Vite)** frontend tracking transaction states in real-time.

---

## System Architecture & Tech Stack

### Frontend
* **React.js (Vite):** Next-gen client build tool utilizing fast hot-module replacement (HMR).
* **TypeScript:** Type-safe development enforcing structured entity modeling.
* **Tailwind CSS:** Fully responsive, utility-first UI design system.
* **Axios:** Component-level networking configured with Server-Side Rendering (SSR) fallback guards.

### Backend
* **FastAPI:** High-performance, asynchronous Python web framework built on ASGI.
* **Pydantic:** Structural validation layers for database payloads and endpoints.
* **Sentence-Transformers:** Local open-source ML embeddings pipeline converting natural text queries into 384-dimensional dense vectors.

### Database
* **MongoDB Atlas Cloud Cluster:** Multi-collection NoSQL cloud datastore.
* **Atlas Vector Search Engine:** Advanced similarity search utilizing Approximate Nearest Neighbors (ANN) vector indexing.

---

## Repository Structure

```text
FoodNow/
├── venv/                       # Python virtual environment (Root Folder)
├── backend/                    # FastAPI Backend Application
│   ├── config/
│   │   ├── db.py               # Database connections (with custom TLS/SSL bypasses)
│   │   └── embeddings.py       # Sentence-transformers pipeline loader
│   ├── routes/
│   │   └── search.py           # Unified router (AI Vector search, Orders, Feedback, Recommendations)
│   ├── services/
│   │   ├── search.py           # Core vector aggregation and text search fallback pipelines
│   │   ├── recommendations.py  # Smart Pair-Up cross-sell matching engine 🚀
│   │   └── orders.py           # Checkout transactional pipelines
│   ├── schemas/
│   │   └── search.py           # Pydantic data schemas (DishResponse mapping)
│   └── main.py                 # FastAPI system entry point with async model warmups
│
└── frontend/                   # React Frontend Application
    ├── src/
    │   ├── contexts/
    │   │   └── AppContext.tsx  # Global state manager (Cart, User Context, Active Orders)
    │   ├── services/
    │   │   └── api.ts          # Axios network core configured with SSR safety layers
    │   └── components/
    │       └── spice/
    │           ├── CustomerApp.tsx # Core consumer interface dashboard & recommendations module
    │           └── DishCard.tsx    # Menu item rendering engine with fallback mapping keys
    └── vite.config.ts

```

---

## ⚙️ Step-by-Step Local Installation & Setup

Follow these setup steps precisely to clone, install, configure, and launch the entire ecosystem locally.

### Prerequisites

* **Python 3.10+** configured in your environment path.
* **Node.js (v18+)** along with `npm`.
* A **MongoDB Atlas Account** with a live cluster provisioning cloud data access.

---

### 1. Database & Index Provisioning

1. Log into your MongoDB Atlas Dashboard.
2. Select your targeted cluster instance and access the **Browse Collections** tab.
3. Ensure you have a target application database named `food_db` containing a collection named `dishes`.
4. Click on the **Atlas Search** tab, select **Create Search Index**, choose **JSON Editor**, and target your `dishes` collection. Name the index exactly `menu_vector_index` and map this structural setup config:

```json
{
  "fields": [
    {
      "numDimensions": 384,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}

```

---

### 2. Environment Variables Integration

Create a file named `.env` inside your **`backend/`** directory to keep system access secrets secure:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@food-cluster.ul6dnzz.mongodb.net/?retryWrites=true&w=majority
VITE_API_URL=http://localhost:8000

```

*(Make sure to append your specific database account credentials into the matching template URI fields above).*

---

### 3. Setting Up and Launching the Backend

Open a terminal instance inside the root directory (`FoodNow/`) and run these shell commands:

```bash
# 1. Initialize the Python Virtual Environment inside the root directory
python -m venv venv

# 2. Activate the virtual environment context (Windows)
.\venv\Scripts\activate

# 3. Navigate directly into the backend workspace
cd backend

# 4. Install all essential Python packages and neural network drivers
pip install -r requirements.txt

# 5. Launch the backend ecosystem using the Uvicorn ASGI engine
python main.py

```

> **Performance Note:** On execution, the custom FastAPI startup engine lifespan block will freeze the local shell briefly to load the local `sentence-transformers` vector tensors into system storage runtime memory. This eliminates incoming client network request latencies.

---

### 4. Setting Up and Launching the Frontend

Open a separate, dedicated terminal window in the root directory (`FoodNow/`) and run these script commands:

```bash
# 1. Navigate straight to the user client interface app
cd frontend

# 2. Extract and install all declared package assets and dependencies
npm install

# 3. Boot up the high-speed Vite local development engine
npm run dev

```

Once initialized, access the interface application at `http://localhost:5173` inside your local web browser.

---

## Core Features & Deep Implementations

### AI-Powered Semantic Vector Search

Utilizes cosine similarity calculations between text prompts and pre-generated item metadata embeddings. If a query misses explicit structural keys, the backend automatically cascades down into localized regex string scanners to shield user query paths against zero-result screens.

### Smart Pair-Up Recommendations (New Feature)

Monitors real-time mutations to user cart arrays. The system tracks item identities, categories, and dietary markers (`vegetarian`, `non-vegetarian`, `spicy`, `light`, `heavy`) inside `frontend/src/components/spice/CustomerApp.tsx` and ships them over to the `/api/cart/recommend` endpoint dynamically. The engine handles automated cross-selling validations (e.g., matching a heavy main course with light soups, or a spicy appetizer with cooling bread options), returning an automated helper suggestion overlay inside the cart drawer.

### Key Technical Implementations Solved

* **FastAPI Lifespan Startup Warmups:** Integrated modern async contextual lifespans to cache neural network model parameters into system memory before opening public local socket endpoints.
* **Network TLS/SSL Bypass Layers:** Formulated network infrastructure socket configuration overlays directly into PyMongo clients to mitigate firewall/ISP TLS packet drops against remote Atlas nodes.
* **Isomorphic SSR Contextual Guards:** Remediated explicit evaluation errors during Vite server-rendering loops by isolating client-only references (`localStorage`, `window`) behind validation flags.
* **Strict Structural API Mappings:** Standardized multi-key payload fallbacks (`dish_id`, `id`, `tags`) mapping seamlessly between MongoDB cursors, Pydantic type specifications, and downstream user interfaces.

```

```
