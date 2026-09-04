FROM python:3.11-slim

WORKDIR /app

# Install compilation tools for XGBoost & C-extensions if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files and static frontend
COPY backend/ backend/

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["python", "backend/main.py"]
