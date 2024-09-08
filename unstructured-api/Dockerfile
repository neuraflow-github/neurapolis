FROM python:3.12-slim
WORKDIR /base
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev
COPY . .
WORKDIR /base/src/unstructured_api
ENV PYTHONPATH=/base/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
