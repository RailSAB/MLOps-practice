FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn scikit-learn pandas numpy joblib


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
