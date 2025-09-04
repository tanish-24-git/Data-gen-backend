# Service for creating embeddings asynchronously
# Supports OpenAI or Gemini (preferred)
from app.utils.config import Config
from app.utils.logger import logger

# Async clients
if Config.MODEL_PROVIDER == "openai":
    from openai import AsyncOpenAI
    openai_client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
elif Config.MODEL_PROVIDER == "gemini":
    import google.generativeai as genai
    genai.configure(api_key=Config.GEMINI_API_KEY)

async def create_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    """
    Async function to generate embeddings.
    - Uses task_type for Gemini to optimize (e.g., RETRIEVAL_DOCUMENT for upsert, RETRIEVAL_QUERY for search).
    - Dimension set to 768 to match Pinecone (assume recreated as per previous advice).
    """
    try:
        if Config.MODEL_PROVIDER == "openai":
            response = await openai_client.embeddings.create(
                model="text-embedding-3-large",
                input=text,
                dimensions=768  # Match Pinecone index dimension
            )
            embedding = response.data[0].embedding
        elif Config.MODEL_PROVIDER == "gemini":
            # Async embed for Gemini
            result = await genai.embed_content_async(
                model="models/text-embedding-004",
                content=text,
                task_type=task_type,
                output_dimensionality=768  # Match Pinecone
            )
            embedding = result['embedding']
        logger.info("Embedding created successfully.")
        return embedding
    except Exception as e:
        logger.error(f"Embedding creation error: {str(e)}")
        raise