# Main entry point for the FastAPI application
# Handles lifespan events for async resources (e.g., Pinecone, Redis)
from contextlib import asynccontextmanager
from app.utils.config import load_config
from app.utils.logger import setup_logger

load_config()  # Load environment variables from .env
setup_logger()  # Initialize logging

# Import FastAPI and middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.api.routes import router

# Import async clients
from pinecone.grpc import PineconeGRPC as PineconeAsyncio  # For async Pinecone
import aioredis

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.
    - Initializes async clients for Pinecone and Redis on startup.
    - Closes them on shutdown to prevent resource leaks.
    """
    # Startup: Configure Gemini if used
    if Config.MODEL_PROVIDER == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
    
    # Initialize async Pinecone client
    app.state.pc = PineconeAsyncio(api_key=Config.PINECONE_API_KEY)
    app.state.index = app.state.pc.Index(Config.PINECONE_INDEX_NAME)
    
    # Initialize async Redis client
    app.state.redis = aioredis.from_url(Config.REDIS_URL, decode_responses=True)
    
    yield  # Yield control to the app
    
    # Shutdown: Close connections
    await app.state.redis.close()
    app.state.pc.close()

# Create FastAPI app with lifespan
app = FastAPI(title="Synthetic Dataset Generator", lifespan=lifespan)

# Set up rate limiter (20 req/min, burst 5/10s per IP)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Add CORS middleware for frontend (e.g., Vercel-hosted)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)