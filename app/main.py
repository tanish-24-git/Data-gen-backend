# Main entry point for the FastAPI application
# Handles lifespan events for async resources (e.g., Pinecone)
from contextlib import asynccontextmanager
from app.utils.config import load_config, Config
from app.utils.logger import setup_logger
import os

# Load environment variables and configure logging
load_config()
setup_logger()

# Import FastAPI and middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware

from app.api.routes import router

# Import async clients
from pinecone import Pinecone

from app.utils.limiter import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.
    - Initializes async clients for Pinecone on startup.
    """
    if Config.MODEL_PROVIDER.lower() == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
    app.state.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
    app.state.index = app.state.pc.Index(Config.PINECONE_INDEX_NAME)
    yield

app = FastAPI(title="Synthetic Dataset Generator", lifespan=lifespan)

# Set up rate limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://data-gen-frontend-git-main-tanish-24-gits-projects.vercel.app,https://data-gen-frontend.vercel.app").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))  # Use Render's PORT env var
    uvicorn.run(app, host="0.0.0.0", port=port)
