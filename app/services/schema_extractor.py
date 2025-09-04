# Service to extract schema from file or prompt
import pandas as pd
from io import StringIO
from app.utils.logger import logger

def extract_schema(input_data: str, is_file: bool = True) -> tuple[str, str]:
    """
    Extracts schema (columns) and description from CSV file content or prompt string.
    Handles structured prompts (e.g., 'field: type') and simple lists (e.g., 'Name, Age, City').
    """
    try:
        if is_file:
            df = pd.read_csv(StringIO(input_data))
            columns = df.columns.tolist()
            schema = ", ".join(columns)
            description = "Sample dataset with columns: " + schema
            logger.info(f"Extracted schema from file: {schema}")
            return schema, description

        # Handle prompt-based input
        logger.info(f"Parsing prompt: {input_data}")
        description = input_data.strip()
        columns = []

        # Clean and normalize prompt
        cleaned_input = input_data.lower().replace(" and ", ", ").replace("for ", "").replace("with ", "").strip(".")
        
        # Extract columns from prompt (e.g., "Name, Age, City" or "id: integer, name: string")
        if "," in cleaned_input:
            # Handle simple comma-separated fields
            columns = [col.strip() for col in cleaned_input.split(",") if col.strip()]
            # Remove any trailing format specification
            columns = [col for col in columns if not col.startswith("format:")]
        elif ":" in cleaned_input:
            # Handle structured format (e.g., "id: integer, name: string")
            for part in cleaned_input.split(","):
                if ":" in part:
                    field = part.split(":")[0].strip()
                    columns.append(field)
                else:
                    columns.append(part.strip())
        
        # If no columns found, try extracting from description
        if not columns:
            # Fallback: look for common patterns in the prompt
            for keyword in ["generate", "dataset", "data", "sample", "records"]:
                cleaned_input = cleaned_input.replace(keyword, "").strip()
            columns = [col.strip() for col in cleaned_input.split(",") if col.strip()]
        
        # Ensure unique columns
        columns = list(dict.fromkeys(columns))
        if not columns:
            raise ValueError("No valid columns found in prompt")
        
        schema = ", ".join(columns)
        logger.info(f"Extracted schema from prompt: {schema}, Description: {description}")
        return schema, description

    except Exception as e:
        logger.error(f"Schema extraction error: {str(e)}")
        raise ValueError(f"Invalid prompt format: {str(e)}")