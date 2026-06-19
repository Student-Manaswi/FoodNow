import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# Secure token from your Hugging Face Account settings
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize the serverless API cluster worker
client = InferenceClient(token=HF_TOKEN)

def get_embedding(text: str) -> list:
    """
    Generates a 384-dimensional dense vector via the 
    Hugging Face cloud service seamlessly.
    """
    if not text or text.strip() == "":
        return [0.0] * 384
        
    try:
        # Request features directly from the matching MiniLM model matrix
        embedding = client.feature_extraction(
            text, 
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Handle structural list dimensions gracefully if wrapped by the API
        if isinstance(embedding, list) and len(embedding) > 0 and isinstance(embedding[0], list):
            return [float(x) for x in embedding[0]]
            
        return [float(x) for x in embedding]
        
    except Exception as e:
        print(f"⚠️ Hugging Face API Fallback Triggered: {e}")
        # Return a zero-vector so downstream database lookups don't crash
        return [0.0] * 384