# Service for hybrid data generation (Faker + Gemini)
# Handles batching, validation, anonymization
from app.utils.config import Config
from app.utils.logger import logger
from faker import Faker
import google.generativeai as genai
import csv
from io import StringIO
from email_validator import validate_email, EmailNotValidError
import re
from typing import List, Dict, AsyncGenerator

fake = Faker()

# Gemini model (preferred)
if Config.MODEL_PROVIDER == "gemini":
    model = genai.GenerativeModel("gemini-1.5-flash")

async def hybrid_generate_synthetic_data_stream(
    num_rows: int, 
    columns: List[str], 
    domain: str, 
    context: str, 
    format: str
) -> AsyncGenerator[List[Dict[str, str]], None]:
    """
    Async generator for hybrid data streaming.
    - Classifies columns: simple (Faker) vs complex (LLM).
    - Generates in batches (10k rows) for large datasets.
    - Validates each row after generation.
    - Yields batches of dict rows (for further formatting/anonymization).
    """
    # Simple fields mapping (Faker for structured data)
    simple_map = {
        'name': fake.name,
        'age': lambda: str(fake.random_int(min=18, max=90)),
        'city': fake.city,
        'email': fake.email,
        'phone': fake.phone_number,
        # Extend with more mappings as needed
    }

    # Classify columns (case-insensitive)
    simple_cols = [col for col in columns if col.lower() in simple_map]
    complex_cols = [col for col in columns if col not in simple_cols]

    batch_size = 10000  # Batch for large datasets to avoid memory issues
    for start in range(0, num_rows, batch_size):
        current_size = min(batch_size, num_rows - start)
        
        # Generate simple data with Faker
        simple_data = [{col: simple_map[col.lower()]() for col in simple_cols} for _ in range(current_size)]

        # Generate complex data with Gemini LLM (async)
        complex_data = []
        if complex_cols:
            llm_prompt = f"Generate {current_size} rows of realistic and diverse values for columns: {', '.join(complex_cols)}\nDomain: {domain}\nSimilar contexts: {context}\nOutput as CSV without header, one row per line."
            response = await model.generate_content_async(llm_prompt)
            generated_text = response.text.strip()
            reader = csv.reader(StringIO(generated_text))
            complex_data = [dict(zip(complex_cols, row)) for row in reader if len(row) == len(complex_cols)]  # Skip invalid

            # Handle if LLM returns fewer rows
            while len(complex_data) < current_size:
                complex_data.append({col: '' for col in complex_cols})  # Fallback, or regenerate batch

        # Combine simple + complex into rows
        batch = []
        for i in range(current_size):
            row = {**simple_data[i], **(complex_data[i] if i < len(complex_data) else {col: '' for col in complex_cols})}
            validated_row = validate_row(row, columns)  # Sync validation (can make async if heavy)
            batch.append(validated_row)

        yield batch  # Yield batch for streaming

def validate_row(row: Dict[str, str], columns: List[str]) -> Dict[str, str]:
    """
    Validates a single row.
    - Checks data types, realism (e.g., age range, valid email).
    - Regenerates invalid fields with Faker.
    """
    for col in columns:
        value = row.get(col, '')
        col_lower = col.lower()
        if 'age' in col_lower:
            try:
                age = int(value)
                if not 0 < age < 120:
                    raise ValueError("Invalid age")
            except ValueError:
                row[col] = str(fake.random_int(18, 90))  # Regenerate
        elif 'email' in col_lower:
            try:
                validate_email(value)
            except EmailNotValidError:
                row[col] = fake.email()  # Regenerate
        # Add more validation rules (e.g., phone regex, no PII unless allowed)
    return row

def anonymize_data(row: Dict[str, str]) -> Dict[str, str]:
    """
    Anonymizes PII in a row (e.g., emails, names).
    - Assumes synthetic data, but applies basic rules.
    """
    for key, value in row.items():
        # Replace emails
        if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', str(value)):
            row[key] = 'anonymous@email.com'
        # Add more rules (e.g., SSN, phones)
    return row