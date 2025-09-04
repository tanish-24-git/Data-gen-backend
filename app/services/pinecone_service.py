# app/services/pinecone_service.py
from app.utils.logger import logger
from pinecone import Pinecone
from fastapi.concurrency import run_in_threadpool

async def upsert_to_pinecone(index, id: str, embedding: list[float], metadata: dict):
    """
    Async wrapper around synchronous Pinecone upsert using run_in_threadpool.
    """
    try:
        response = await run_in_threadpool(index.upsert, vectors=[(id, embedding, metadata)])
        logger.info(f"Upserted to Pinecone: {id}")
        return response
    except Exception as e:
        logger.error(f"Pinecone upsert error: {str(e)}")
        raise


async def query_pinecone(index, embedding: list[float], top_k: int = 5) -> dict:
    """
    Async wrapper around synchronous Pinecone query using run_in_threadpool.
    """
    try:
        results = await run_in_threadpool(index.query, vector=embedding, top_k=top_k, include_metadata=True)
        logger.info("Pinecone query successful.")
        return results
    except Exception as e:
        logger.error(f"Pinecone query error: {str(e)}")
        raise
