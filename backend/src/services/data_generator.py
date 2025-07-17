# Service for generating synthetic data using Google Gemini and Faker
import google.generativeai as genai
from faker import Faker
from src.models.schemas import DatasetRequest
from src.config import config
import json
import random

class DataGenerator:
    def __init__(self, logger):
        # Use the logger passed from the calling context
        self.logger = logger
        self.faker = Faker()
        self.llm = genai.GenerativeModel(config.GEMINI_MODEL_NAME)

    def create_prompt(self, columns, row_count):
        schema = {col.name: col.type for col in columns}
        examples_str = ""
        instructions = ""
        for col in columns:
            if col.examples:
                examples_str += f"Examples for {col.name}: {json.dumps(col.examples)}\n"
                instructions += f"- The \"{col.name}\" column should contain values randomly selected from the examples: {', '.join(map(str, col.examples))}.\n"
        
        prompt = (
            "Generate synthetic data in JSON format based on the following schema and examples.\n"
            f"Schema: {json.dumps(schema)}\n"
            f"{examples_str}"
            f"Generate {row_count} rows of data where:\n"
            f"{instructions}"
            "The output should be a JSON array of objects, each with the specified fields."
        )
        return prompt
    
    def generate_data(self, request: DatasetRequest) -> list:
        prompt = self.create_prompt(request.columns, request.row_count)
        try:
            # Generate data using Gemini API
            response = self.llm.generate_content(prompt)
            llm_data = json.loads(response.text.strip())  # Parse JSON
            if not isinstance(llm_data, list):
                llm_data = [llm_data]  # Ensure it's a list
            # Validate that each item has all required columns
            required_columns = {col.name for col in request.columns}
            for item in llm_data:
                if not isinstance(item, dict) or not required_columns.issubset(item.keys()):
                    raise ValueError("Invalid data format from Gemini API")
        except Exception as e:
            self.logger.error(f"Gemini generation failed: {str(e)}")
            # Fallback to updated Faker method if Gemini fails
            llm_data = self.generate_fallback_data(request)
        return llm_data
    
    def generate_fallback_data(self, request: DatasetRequest) -> list:
        # Fallback data generation using provided examples if available
        data = []
        for _ in range(request.row_count):
            row = {}
            for col in request.columns:
                if col.examples:
                    # Randomly select from examples
                    row[col.name] = random.choice(col.examples)
                else:
                    # If no examples, use Faker
                    if col.type == "string":
                        row[col.name] = self.faker.word()
                    elif col.type == "integer":
                        row[col.name] = self.faker.random_int(min=1, max=1000)
                    elif col.type == "float":
                        row[col.name] = round(self.faker.random_number(digits=5) / 100, 2)
            data.append(row)
        return data

    def enhance_with_faker(self, data: list, columns: list) -> list:
        # Enhance Gemini-generated data with Faker for realistic patterns
        for row in data:
            for col in columns:
                if col.name in row:
                    if col.type == "string" and not row[col.name]:
                        row[col.name] = self.faker.name() if col.name.lower().find("name") != -1 else self.faker.word()
                    elif col.type == "integer" and not row[col.name]:
                        row[col.name] = self.faker.random_int(min=1, max=1000)
                    elif col.type == "float" and not row[col.name]:
                        row[col.name] = round(self.faker.random_number(digits=5) / 100, 2)
        return data