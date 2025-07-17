# API routes for dataset generation
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from src.models.schemas import DatasetRequest
from src.services.data_generator import DataGenerator
from src.logger import setup_logger
from src.utils.helpers import verify_api_key
import pandas as pd
import os
import tempfile

router = APIRouter(prefix="/api/v1", tags=["dataset"])

@router.post("/generate", response_class=FileResponse)
async def generate_dataset(request: DatasetRequest, _: bool = Depends(verify_api_key)):
    # Generate synthetic dataset based on user input and return as CSV
    logger = setup_logger("DatasetGenerator")  # Initialize logger with a specific name
    logger.info(f"Received request to generate dataset with {request.row_count} rows")
    
    try:
        # Generate the dataset
        generator = DataGenerator(logger)  # Pass logger instance to DataGenerator
        data = generator.generate_data(request)
        
        # Convert dataset to DataFrame
        df = pd.DataFrame(data)
        
        # Create a temporary file to store the CSV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            df.to_csv(temp_file.name, index=False)
        
        # Set response headers for file download
        headers = {
            "Content-Disposition": f"attachment; filename=synthetic_dataset.csv"
        }
        
        # Return the CSV file as a downloadable response
        response = FileResponse(
            path=temp_file.name,
            filename="synthetic_dataset.csv",
            media_type="text/csv",
            headers=headers
        )
        # Cleanup: Remove the temporary file after the response is sent
        def cleanup():
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
        response.close = cleanup  # Override close method to clean up file
        return response
    except Exception as e:
        logger.error(f"Error generating dataset: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")