import pandas as pd
from io import StringIO
from app.utils.logger import logger

def extract_schema(input_data: str, is_file: bool = True) -> tuple:
    """
    Extracts schema and description from CSV or prompt.
    Returns (schema_str, description)
    """
    try:
        if is_file:
            df = pd.read_csv(StringIO(input_data))
            columns = df.columns.tolist()
            schema = ", ".join(columns)
            description = "Sample dataset with columns: " + schema
        else:
            # Parse prompt, e.g., extract columns from "Generate ... with Name, Age, ..."
            parts = input_data.lower().split("with")
            if len(parts) > 1:
                columns = [col.strip() for col in parts[1].split(",")]
                schema = ", ".join(columns)
                description = input_data
            else:
                raise ValueError("Invalid prompt format.")
        
        logger.info(f"Extracted schema: {schema}")
        return schema, description
    except Exception as e:
        logger.error(f"Schema extraction error: {str(e)}")
        raise