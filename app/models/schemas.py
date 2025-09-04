# Pydantic models for request/response validation
from pydantic import BaseModel, field_validator

class GenerationRequest(BaseModel):
    """
    Model for validating generation requests.
    Ensures num_rows is positive and format is valid.
    """
    prompt: str | None = None
    num_rows: int = 1000
    format: str = "csv"

    @field_validator('num_rows')
    @classmethod
    def num_rows_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('num_rows must be positive')
        return v

    @field_validator('format')
    @classmethod
    def format_valid(cls, v: str) -> str:
        if v not in ['csv', 'json']:
            raise ValueError('format must be csv or json')
        return v

class GenerationResponse(BaseModel):
    """
    Model for response (though now streaming, kept for reference).
    """
    download_link: str
    message: str