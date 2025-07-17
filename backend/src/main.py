# Main entry point for the FastAPI application
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from src.routes.dataset import router as dataset_router
from src.logger import setup_logger
from src.utils.helpers import verify_api_key
import uvicorn
import logging

# Initialize logger globally
logger = setup_logger("SyntheticDatasetGenerator")

# Lifespan event handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Startup logic
        logger.info("Starting Synthetic Dataset Generator API")
        yield
    except Exception as e:
        logger.error(f"Error during startup or shutdown: {str(e)}")
        raise
    finally:
        # Shutdown logic
        logger.info("Shutting down Synthetic Dataset Generator API")

# Initialize FastAPI app with custom Swagger UI settings
app = FastAPI(
    title="Synthetic Dataset Generator API",
    description="API for generating synthetic datasets using Google Gemini and Faker",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (including x-api-key)
)

# Include dataset routes (for /api/v1/generate)
app.include_router(dataset_router)

# Root endpoint for basic API info
@app.get("/")
async def root():
    return {"message": "Welcome to the Synthetic Dataset Generator API. Visit /docs for API documentation."}

# Protect Swagger UI with API key
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(api_key: str = Depends(verify_api_key)):
    from fastapi.responses import HTMLResponse
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Synthetic Dataset Generator API - Swagger UI",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}
    )

# Protect OpenAPI JSON endpoint with API key
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint(api_key: str = Depends(verify_api_key)):
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)