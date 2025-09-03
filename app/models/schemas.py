from pydantic import BaseModel

class GenerationRequest(BaseModel):
    prompt: str | None = None
    num_rows: int = 1000
    format: str = "csv"

class GenerationResponse(BaseModel):
    download_link: str
    message: str