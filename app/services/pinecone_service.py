# Async service for Pinecone operations
# Only stores metadata and embeddings, no raw data
from app.utils.logger import logger
from pinecone import Pinecone # Assuming app.state.index is GRPC index

async def upsert_to_pinecone(index, id: str, embedding: list[float], metadata: dict):
    """
    Async upsert to Pinecone.
    - Stores dataset_id, columns, description, privacy, domain.
    """
    try:
        await index.upsert(vectors=[(id, embedding, metadata)])
        logger.info(f"Upserted to Pinecone: {id}")
    except Exception as e:
        logger.error(f"Pinecone upsert error: {str(e)}")
        raise

async def query_pinecone(index, embedding: list[float], top_k: int = 5) -> dict:
    """
    Async query for similar embeddings.
    - Returns top_k results with metadata for context.
    """
    try:
        results = await index.query(vector=embedding, top_k=top_k, include_metadata=True)
        logger.info("Pinecone query successful.")
        return results
    except Exception as e:
        logger.error(f"Pinecone query error: {str(e)}")
        raise