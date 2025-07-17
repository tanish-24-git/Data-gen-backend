# Pydantic models for request/response validation
from pydantic import BaseModel
from typing import List, Dict, Any

class ColumnSchema(BaseModel):
    name: str
    type: str  # e.g., "string", "integer", "float"
    examples: List[Any]  # Few-shot examples for LLM

class DatasetRequest(BaseModel):
    columns: List[ColumnSchema]
    row_count: int

class DatasetResponse(BaseModel):
    data: List[Dict[str, Any]]
    message: str