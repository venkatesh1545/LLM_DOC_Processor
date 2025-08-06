#!/bin/bash
set -e

echo "Starting Ollama server..."
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 10

# Pull the required model
echo "Pulling llama3:latest model..."
ollama pull llama3:latest

echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 1
