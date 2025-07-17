@echo off
:: Setup script for initializing the project environment on Windows with Google Gemini

echo Setting up Synthetic Dataset Generator...

:: Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt

echo Setup complete. Update .env with your GEMINI_API_KEY and API_KEY, then run 'python -m src.main'