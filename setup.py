from setuptools import setup, find_packages

setup(
    name='synthetic-dataset-platform',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'pandas',
        'openai',
        'pinecone',
        'python-dotenv',
        'python-multipart',
    ],
    entry_points={
        'console_scripts': [
            'run-app = app.main:run',
        ]
    },
)