# Standard setup script for packaging the application
from setuptools import setup, find_packages

setup(
    name='synthetic-dataset-platform',  # Project name
    version='0.1.0',  # Initial version
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[  # Dependencies (mirrors requirements.txt for pip install -e .)
        'fastapi',
        'uvicorn',
        'pydantic',
        'pandas',
        'openai',
        'google-generativeai',
        'pinecone-client[asyncio]',
        'python-dotenv',
        'python-multipart',
        'faker',
        'slowapi',
        'email-validator',
        'bleach',
    ],
    entry_points={  # Console script entry points
        'console_scripts': [
            'run-app = app.main:run',  # Allows running 'run-app' from command line
        ]
    },
)