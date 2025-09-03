```
synthetic-dataset-platform/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entry point for FastAPI app
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py            # API endpoints/routers
│   ├── services/
│   │   ├── __init__.py
│   │   ├── schema_extractor.py  # Extracts schema from CSV or prompt
│   │   ├── embedding_service.py # Handles embeddings with OpenAI/HuggingFace
│   │   ├── pinecone_service.py  # Interacts with Pinecone
│   │   ├── llm_generator.py     # Uses LLM to generate synthetic data
│   │   └── privacy_handler.py   # Handles PII removal and compliance
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py            # Centralized logging setup
│   │   ├── config.py            # Loads .env configs
│   │   └── helpers.py           # Misc helpers (e.g., CSV parsing, file handling)
│   └── models/
│       ├── __init__.py
│       └── schemas.py           # Pydantic models for API requests/responses
├── tests/
│   ├── __init__.py
│   └── test_services.py         # Unit tests (stubbed)
├── .env                         # Environment variables (git ignore this)
├── .gitignore                   # Standard gitignore
├── requirements.txt             # Dependencies
├── setup.py                     # For packaging the app
└── README.md                    # Project docs