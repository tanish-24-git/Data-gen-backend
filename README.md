```
synthetic-dataset-platform/
├── README.md
├── requirements.txt
├── setup.py
├── app/
│   ├── __init__.py  (empty)
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py  (empty)
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py  (empty)
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py  (empty)
│   │   ├── embedding_service.py
│   │   ├── llm_generator.py
│   │   ├── pinecone_service.py
│   │   └── schema_extractor.py
│   └── utils/
│       ├── __init__.py  (empty)
│       ├── config.py
│       └── logger.py
└── tests/
    └── test_services.py

```