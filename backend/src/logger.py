# src/logger.py
import logging
import os
from src.config import config

def setup_logger(name):
    # Create a logger with the specified name
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Create file handler for logging to a file
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Create console handler for logging to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Define log message format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger