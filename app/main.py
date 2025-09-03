from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # Added for CORS
from app.api.routes import router
from app.utils.logger import setup_logger
from app.utils.config import load_config

load_config()  # Load .env
setup_logger()  # Setup logging

app = FastAPI(title="Synthetic Dataset Generator")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Allow Next.js dev server; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for downloads (create temp_files dir)
app.mount("/temp_files", StaticFiles(directory="temp_files"), name="temp_files")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)