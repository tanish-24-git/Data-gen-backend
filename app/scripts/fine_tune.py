"""
Script to fine-tune an OpenAI model for synthetic dataset generation.
Run: python scripts/fine_tune.py --training_file path/to/train.jsonl --model gpt-4o-mini

Requires: openai library (already in requirements.txt)
"""

import argparse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_training_file(file_path: str):
    with open(file_path, "rb") as f:
        response = client.files.create(file=f, purpose="fine-tune")
    print(f"Uploaded file ID: {response.id}")
    return response.id

def create_fine_tuning_job(training_file_id: str, model: str = "gpt-4o-mini"):
    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model=model
    )
    print(f"Fine-tuning job created: {response.id}")
    print("Monitor status in OpenAI dashboard or via API.")
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune OpenAI model.")
    parser.add_argument("--training_file", required=True, help="Path to JSONL training file")
    parser.add_argument("--model", default="gpt-4o-mini", help="Base model to fine-tune")
    args = parser.parse_args()

    file_id = upload_training_file(args.training_file)
    create_fine_tuning_job(file_id, args.model)