import os
from app.utils.config import Config
from app.utils.logger import logger
import csv
import json
from io import StringIO

if Config.MODEL_PROVIDER == "openai":
    from openai import OpenAI
    openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
elif Config.MODEL_PROVIDER == "gemini":
    import google.generativeai as genai
    genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_synthetic_data(prompt: str, format: str = "csv") -> str:
    try:
        if Config.MODEL_PROVIDER == "openai":
            model = Config.FINE_TUNED_MODEL or "gpt-4o-mini"
            response = openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            generated_text = response.choices[0].message.content.strip()
        elif Config.MODEL_PROVIDER == "gemini":
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            generated_text = response.text.strip()
        else:
            raise ValueError("Unsupported model provider.")

        # Parse output to structured data
        if format == "csv":
            return generated_text
        elif format == "json":
            return generated_text
        else:
            raise ValueError("Unsupported format.")
    except Exception as e:
        logger.error(f"LLM generation error: {str(e)}")
        raise

# For large num_rows, batch: Generate in chunks of 1000, append.