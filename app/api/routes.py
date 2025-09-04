# API routes for the application
# Handles the /generate-dataset endpoint with streaming, caching, async calls
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.services.schema_extractor import extract_schema
from app.services.embedding_service import create_embedding
from app.services.pinecone_service import upsert_to_pinecone, query_pinecone
from app.services.llm_generator import hybrid_generate_synthetic_data_stream, anonymize_data
from app.models.schemas import GenerationRequest  # For Pydantic validation
from app.utils.logger import logger
import bleach  # For input sanitization
import hashlib  # For cache key hashing
from typing import AsyncGenerator

router = APIRouter()

@router.post("/generate-dataset")
@router.app.state.limiter.limit("20/minute;5/10second")  # Apply rate limiting
async def generate_dataset(
    request: Request,
    prompt: str = Form(None),
    file: UploadFile = File(None),
    num_rows: int = Form(1000),
    format: str = Form("csv")  # csv or json (streams as NDJSON)
) -> StreamingResponse:
    """
    Endpoint to generate synthetic dataset.
    - Validates inputs with Pydantic.
    - Sanitizes prompt.
    - Checks cache for small requests.
    - Streams data in batches without storage.
    - Uses async for external calls.
    """
    try:
        # Pydantic validation (via GenerationRequest, but since Form, manual)
        GenerationRequest(prompt=prompt, num_rows=num_rows, format=format)  # Raises if invalid

        if not prompt and not file:
            raise HTTPException(status_code=400, detail="Provide either prompt or file.")

        # Sanitize prompt if provided
        if prompt:
            prompt = bleach.clean(prompt)  # Prevent injection
            if len(prompt) > 2000:
                raise HTTPException(status_code=400, detail="Prompt too long (max 2000 characters).")

        # Extract schema and description
        if file:
            content = await file.read()
            content = content.decode('utf-8')
            schema, description = extract_schema(content, is_file=True)
        else:
            schema, description = extract_schema(prompt, is_file=False)

        # Create embedding async
        schema_text = f"{schema} - {description}"
        embedding = await create_embedding(schema_text, task_type="RETRIEVAL_DOCUMENT")

        # Metadata for Pinecone (no raw data stored)
        metadata = {
            "domain": "general",  # Infer or from prompt (TODO: improve inference)
            "columns": schema.split(", "),
            "description": description,
            "privacy": "public"
        }
        dataset_id = f"dataset_{hash(schema_text)}"  # Unique ID

        # Async upsert to Pinecone
        await upsert_to_pinecone(request.app.state.index, dataset_id, embedding, metadata)

        # Async query Pinecone for similar contexts
        query_embedding = await create_embedding(schema_text, task_type="RETRIEVAL_QUERY")
        similar_results = await query_pinecone(request.app.state.index, query_embedding, top_k=3)
        context = "\n".join([res['metadata'].get('description', '') for res in similar_results.get('matches', [])])

        # Cache key based on request params
        cache_key = hashlib.sha256(f"{schema}{description}{num_rows}{format}{context}".encode()).hexdigest()

        # Check Redis cache if small request (<=10k rows)
        if num_rows <= 10000:
            cached_data = await request.app.state.redis.get(cache_key)
            if cached_data:
                logger.info("Serving from cache")
                def cache_stream() -> AsyncGenerator[str, None]:
                    for line in cached_data.splitlines(keepends=True):
                        yield line
                media_type = 'text/csv' if format == 'csv' else 'application/ndjson'
                return StreamingResponse(cache_stream(), media_type=media_type, headers={"Content-Disposition": f"attachment; filename=dataset.{format}"})

        # Stream generator: hybrid generation with batching, validation, anonymization
        async def data_stream() -> AsyncGenerator[str, None]:
            columns_list = schema.split(", ")
            if format == 'csv':
                yield ','.join(columns_list) + '\n'  # Header for CSV

            # Get stream from hybrid generator
            async for batch in hybrid_generate_synthetic_data_stream(num_rows, columns_list, metadata['domain'], context, format):
                # Batch is list of dicts (rows)
                # Anonymize and validate each row
                for row in batch:
                    row = anonymize_data(row)  # Anonymize dict
                    # Validation is already in generator, but can add more here if needed

                # Format and yield lines
                for row in batch:
                    if format == 'csv':
                        line = ','.join([str(row[col]) for col in columns_list])  # Handle quoting if needed
                    else:  # NDJSON for json
                        line = json.dumps(row)
                    yield line + '\n'

            # Cache full response if small (collect in memory for caching)
            if num_rows <= 10000:
                # Note: For caching streaming, we'd need to collect, but skip for large; implement buffer if needed
                pass

        media_type = 'text/csv' if format == 'csv' else 'application/ndjson'
        return StreamingResponse(data_stream(), media_type=media_type, headers={"Content-Disposition": f"attachment; filename=dataset.{format}"})

    except Exception as e:
        logger.error(f"Error generating dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))