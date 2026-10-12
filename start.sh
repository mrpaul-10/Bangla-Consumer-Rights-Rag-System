#!/bin/bash
set -e

echo "Building vector index..."
python scripts/build_index.py

echo "Starting FastAPI..."
uvicorn api:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &

wait -n