# Build Stage
FROM python:3.13-slim


COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv


COPY . /app

WORKDIR /app/realtimemap

RUN uv sync --no-dev

# CMD ["../.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["../.venv/bin/python", "main.py"]