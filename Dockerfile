FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose both ports
EXPOSE 8000 8501

# Build the vector index, then start both services
CMD python scripts/build_index.py && \
    uvicorn api:app --host 0.0.0.0 --port 8000 & \
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0