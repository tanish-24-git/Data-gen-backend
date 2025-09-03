import pinecone
from app.utils.config import Config
from app.utils.logger import logger

pinecone.init(api_key=Config.PINECONE_API_KEY, environment=Config.PINECONE_ENVIRONMENT)
index = pinecone.Index(Config.PINECONE_INDEX_NAME)

def upsert_to_pinecone(id: str, embedding: list, metadata: dict):
    try:
        index.upsert(vectors=[(id, embedding, metadata)])
        logger.info(f"Upserted to Pinecone: {id}")
    except Exception as e:
        logger.error(f"Pinecone upsert error: {str(e)}")
        raise

def query_pinecone(embedding: list, top_k: int = 5) -> dict:
    try:
        results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
        logger.info("Pinecone query successful.")
        return results
    except Exception as e:
        logger.error(f"Pinecone query error: {str(e)}")
        raise