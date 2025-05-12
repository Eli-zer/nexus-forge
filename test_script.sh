#!/bin/bash

# Sanity check script to test the basic setup of NexusForge

echo "Building and starting services..."
docker compose up -d

echo "Waiting for services to start..."
sleep 10

echo "Pulling tinyllama model for testing..."
curl -X POST http://localhost:11434/api/pull -d '{"name": "tinyllama"}'

echo "Testing API Gateway health endpoint..."
curl http://localhost:8000/health

echo "Testing Text-to-Text Service ping endpoint..."
curl http://localhost:8000/api/v1/ping

echo "Testing Ollama by listing models..."
curl http://localhost:8000/api/v1/models

echo "Testing Ollama with a simple prompt..."
curl -X POST "http://localhost:8000/api/v1/simple-prompt?prompt=Hello%20world"

echo "Test complete!"