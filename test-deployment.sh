#!/bin/bash

echo "======================================"
echo "AI Website Generator - Deployment Test"
echo "======================================"

echo ""
echo "[1/6] Stopping existing containers..."
docker-compose down

echo ""
echo "[2/6] Building images..."
docker-compose build

echo ""
echo "[3/6] Starting services..."
docker-compose up -d

echo ""
echo "[4/6] Waiting for services to be ready..."
sleep 15

echo ""
echo "[5/6] Checking service health..."
echo "Frontend: http://localhost:8000"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:8000/

echo "Backend: http://localhost:8001/api/health"
curl -s http://localhost:8001/api/health | jq '.' || echo "Backend not ready"

echo ""
echo "[6/6] Checking logs..."
echo "=== Backend Logs ==="
docker-compose logs backend | tail -20

echo ""
echo "=== PostgreSQL Logs ==="
docker-compose logs postgres | tail -10

echo ""
echo "======================================"
echo "Test URLs:"
echo "  - Frontend:     http://localhost:8000"
echo "  - Corporate:    http://localhost:8000/corporate/"
echo "  - Generator:    http://localhost:8000/generator/"
echo "  - API Docs:     http://localhost:8001/docs"
echo "======================================"
