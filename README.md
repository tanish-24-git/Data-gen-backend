```
synthetic-dataset-platform/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── schema_extractor.py
│   │   ├── embedding_service.py  # Updated for Gemini
│   │   ├── pinecone_service.py
│   │   ├── llm_generator.py     # Updated for Gemini
│   │   └── privacy_handler.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── config.py            # Updated with MODEL_PROVIDER and GEMINI_API_KEY
│   │   └── helpers.py
│   └── models/
│       ├── __init__.py
│       └── schemas.py
├── tests/
│   ├── __init__.py
│   └── test_services.py
├── .env                         # Updated
├── .gitignore
├── requirements.txt             # Updated
├── setup.py
└── README.md                    # Updated