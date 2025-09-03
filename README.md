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
│   │   ├── embedding_service.py  
│   │   ├── pinecone_service.py
│   │   ├── llm_generator.py     
│   │   └── privacy_handler.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── config.py            
│   │   └── helpers.py
│   └── models/
│       ├── __init__.py
│       └── schemas.py
├── tests/
│   ├── __init__.py
│   └── test_services.py
├── .env                         
├── .gitignore
├── requirements.txt             
├── setup.py
└── README.md                    