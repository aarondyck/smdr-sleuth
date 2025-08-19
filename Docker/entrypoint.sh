#!/bin/bash
set -e

# Initialize database if missing
if [ ! -f backend/smdr.db ]; then
  echo "Initializing database..."
  python backend/db_init.py
fi

# Start backend API
echo "Starting FastAPI backend..."
uvicorn backend.api:app --host 0.0.0.0 --port 8000 &

# Start SMDR server
echo "Starting SMDR TCP server..."
python backend/smdr_server.py &

# Start frontend (Vite)
cd web
npm install
npm run dev -- --host 0.0.0.0

wait
