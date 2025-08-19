# Multi-stage build for SMDR Sleuth
FROM python:3.11-slim AS backend
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/ backend/
COPY Docker/entrypoint.sh /app/entrypoint.sh
RUN python backend/db_init.py

FROM node:20 AS frontend
WORKDIR /app/web
COPY web/ /app/web/
RUN npm install && npm run build

FROM python:3.11-slim
WORKDIR /app
COPY --from=backend /app/backend /app/backend
COPY --from=backend /app/entrypoint.sh /app/entrypoint.sh
COPY --from=frontend /app/web/dist /app/web/dist
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN apt-get update && apt-get install -y nodejs npm
EXPOSE 8000 5000 5173
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
