from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.schema_extractor import extract_schema
from app.services.embedding_service import create_embedding
from app.services.pinecone_service import upsert_to_pinecone, query_pinecone
from app.services.llm_generator import generate_synthetic_data
from app.services.privacy_handler import anonymize_data
from app.models.schemas import GenerationRequest, GenerationResponse
from app.utils.helpers import save_temp_csv
from app.utils.logger import logger
import os

router = APIRouter()

@router.post("/generate-dataset", response_model=GenerationResponse)
async def generate_dataset(
    prompt: str = Form(None),
    file: UploadFile = File(None),
    num_rows: int = Form(1000),
    format: str = Form("csv")  # csv or json
):
    try:
        if not prompt and not file:
            raise HTTPException(status_code=400, detail="Provide either prompt or file.")

        # Step 1-2: Extract schema
        if file:
            schema, description = extract_schema_from_file(file)
        else:
            schema, description = extract_schema_from_prompt(prompt)

        # Step 3: Create embedding
        schema_text = f"{schema} - {description}"
        embedding = create_embedding(schema_text)

        # Step 4: Store in Pinecone
        metadata = {
            "domain": "general",  # Infer or from prompt
            "columns": schema.split(", "),
            "description": description,
            "privacy": "public"
        }
        dataset_id = f"dataset_{hash(schema_text)}"  # Unique ID
        upsert_to_pinecone(dataset_id, embedding, metadata)

        # Step 5: Query similar
        similar_results = query_pinecone(embedding, top_k=3)
        context = "\n".join([res['metadata']['description'] for res in similar_results.get('matches', [])])

        # Step 6: Generate with LLM
        llm_prompt = f"Generate a synthetic dataset of {num_rows} rows based on the following schema:\nColumns: {schema}\nDomain: {metadata['domain']}\nSimilar contexts: {context}\nEnsure values are realistic and diverse.\nOutput in {format.upper()} format."
        generated_data = generate_synthetic_data(llm_prompt, format)

        # Privacy handling
        anonymized_data = anonymize_data(generated_data)

        # Step 7: Save and deliver
        if format == "csv":
            file_path = save_temp_csv(anonymized_data)
            download_link = f"/temp_files/{os.path.basename(file_path)}"
        else:
            # For JSON, similar logic
            download_link = ""  # Implement as needed

        return {"download_link": download_link, "message": "Dataset generated successfully."}
    except Exception as e:
        logger.error(f"Error generating dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def extract_schema_from_file(file: UploadFile):
    # Helper to avoid circular imports
    from app.services.schema_extractor import extract_schema
    content = file.file.read().decode()
    return extract_schema(content, is_file=True)

def extract_schema_from_prompt(prompt: str):
    from app.services.schema_extractor import extract_schema
    return extract_schema(prompt, is_file=False)