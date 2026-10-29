FROM node:22-alpine AS frontend
WORKDIR /build/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH=/app/.venv/bin:$PATH \
    PYTHONPATH=/app
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv==0.12.23 \
    && uv sync --locked --no-dev --no-install-project
COPY README.md ./
COPY exam_assistant ./exam_assistant
COPY project-handoff/trees ./project-handoff/trees
COPY --from=frontend /build/frontend/dist ./frontend/dist
RUN uv sync --locked --no-dev
RUN mkdir -p /app/data/uploads && chown -R 10001:10001 /app
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "exam_assistant.api:app", "--host", "0.0.0.0", "--port", "8000"]
