# Utility functions for API key validation and other helpers
from fastapi import HTTPException, Header
from src.config import config
from src.logger import setup_logger

async def verify_api_key(x_api_key: str = Header(...)):
    # Validate API key securely
    logger = setup_logger("APIKeyVerifier")  # Initialize logger with a specific name
    if x_api_key != config.API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key