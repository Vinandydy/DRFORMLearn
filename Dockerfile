FROM python:3.13

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONNUNBUFFERED 1
WORKDIR /drf/app

COPY poetry.lock pyproject.toml /drf/app/

RUN pip install poetry

RUN poetry install --no-root --no-interaction --no-ansi


