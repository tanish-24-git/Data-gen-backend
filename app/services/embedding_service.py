import os
from app.utils.config import Config
from app.utils.logger import logger


if Config.MODEL_PROVIDER == "openai":
    from openai import OpenAI
    openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
elif Config.MODEL_PROVIDER == "gemini":
    import google.generativeai as genai
    genai.configure(api_key=Config.GEMINI_API_KEY)
    from google.genai import types

def create_embedding(text: str) -> list:
    try:
        if Config.MODEL_PROVIDER == "openai":
            response = openai_client.embeddings.create(
                model="text-embedding-3-large",
                input=text
            )
            embedding = response.data[0].embedding
        elif Config.MODEL_PROVIDER == "gemini":
            result = genai.embed_content(
                model="gemini-embedding-001",
                content=text,
                output_dimensionality=3072  # Match Pinecone dimension
            )
            embedding = result['embedding']
        logger.info("Embedding created successfully.")
        return embedding
    except Exception as e:
        logger.error(f"Embedding creation error: {str(e)}")
        raise