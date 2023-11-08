# FastAPI_Celery_Python_MVP
Demonstrating the power of asynchronous task processing in Python

- In ```app``` run ```celery -A celery_worker.celery worker --loglevel=info```
- In ```app``` run ```uvicorn main:app --reload```