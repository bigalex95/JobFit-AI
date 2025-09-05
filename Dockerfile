# Dockerfile for JobFit-AI

# Backend
FROM python:3.11-slim AS backend
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY jobfit-ai/backend ./backend

# Frontend
FROM python:3.11-slim AS frontend
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY jobfit-ai/frontend ./frontend

# Final image (example: backend only)
FROM backend as final
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
