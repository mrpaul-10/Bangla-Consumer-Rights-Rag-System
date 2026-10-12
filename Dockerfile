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
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]