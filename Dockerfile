FROM python:3.12.4-slim

RUN pip install --upgrade pip
RUN pip install poetry==1.8.3

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

ENV \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.3

EXPOSE 8000

WORKDIR /opt/user-management

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR
RUN poetry export --without-hashes -f requirements.txt -o requirements.txt
RUN python3 -m venv venv && . venv/bin/activate
RUN pip install --no-cache-dir --no-deps -r requirements.txt

COPY . .
