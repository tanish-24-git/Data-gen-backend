import os
import csv
from io import StringIO

def save_temp_csv(csv_data: str) -> str:
    os.makedirs("temp_files", exist_ok=True)
    file_path = f"temp_files/generated_{id(csv_data)}.csv"
    with open(file_path, "w") as f:
        f.write(csv_data)
    return file_path