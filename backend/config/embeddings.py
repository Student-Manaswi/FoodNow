from sentence_transformers import SentenceTransformer
import os

# Load once at startup (global instance)
model = None

def load_embedding_model():
    global model
    if model is None:
        print("⏳ Loading sentence-transformers model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded (384-dim vectors)")
    return model

def get_embedding(text: str) -> list:
    """Convert text to 384-dim vector"""
    model = load_embedding_model()
    embedding = model.encode(text)
    return embedding.tolist()  