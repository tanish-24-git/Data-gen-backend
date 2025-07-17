# Configuration management for environment variables and settings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Gemini API configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Google Gemini API key
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")  # Renamed to match DataGenerator expectation, default to Gemini 1.5 Pro
    
    # API key for authentication (stored securely in environment)
    API_KEY = os.getenv("API_KEY")
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "app.log")

# Singleton instance of Config
config = Config()