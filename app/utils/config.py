# Configuration loader from .env
from dotenv import load_dotenv
import os

class Config:
    """
    Config class to hold environment variables.
    - Defaults MODEL_PROVIDER to 'gemini'.
    - Adds REDIS_URL for caching.
    """
    OPENAI_API_KEY = None
    GEMINI_API_KEY = None
    PINECONE_API_KEY = None
    PINECONE_ENVIRONMENT = None
    PINECONE_INDEX_NAME = None
    MODEL_PROVIDER = "gemini"  # Preferred as per requirements
    FINE_TUNED_MODEL = None
    REDIS_URL = None  # For caching

def load_config():
    """
    Loads config from .env.
    - Validates required keys.
    - For deployment: Use Render/Vercel env vars (links in README).
    """
    load_dotenv()
    Config.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    Config.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    Config.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    Config.PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    Config.PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    Config.MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "gemini").lower()
    Config.FINE_TUNED_MODEL = os.getenv("FINE_TUNED_MODEL")
    Config.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")  # Default local
    
    # Validation
    if Config.MODEL_PROVIDER == "gemini" and not Config.GEMINI_API_KEY:
        raise ValueError("Missing GEMINI_API_KEY in .env for Gemini provider")
    if Config.MODEL_PROVIDER == "openai" and not Config.OPENAI_API_KEY:
        raise ValueError("Missing OPENAI_API_KEY in .env for OpenAI provider")