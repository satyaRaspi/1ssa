# Shakti Scheme Application - Railway/Docker deployment
# Builds React frontend and serves it from the FastAPI backend as one service.

FROM node:22-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/.npmrc ./
RUN npm install --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SHAKTI_DB_PATH=/data/shakti_applications.db \
    SHAKTI_UPLOAD_DIR=/data/uploads

WORKDIR /app
RUN mkdir -p /data/uploads

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend/ /app/backend/
COPY README.md CHANGELOG.md VERSION.json /app/
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

WORKDIR /app/backend
EXPOSE 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
