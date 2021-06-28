FROM python:3.8.9-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

RUN apt-get update && \
    apt-get clean && \
    apt-get install -y libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.4

RUN pip install "poetry==${POETRY_VERSION}"
RUN python -m venv /venv
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin
COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM builder as development

RUN poetry export -f requirements.txt --dev | /venv/bin/pip install -r /dev/stdin
COPY alembic.ini scripts/run_tests.sh ./
ENTRYPOINT ["./run_tests.sh"]

FROM base as final

RUN apt-get update && \
    apt-get clean && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv
COPY alembic.ini /app
COPY jwt_authentication_python_postgres /app/jwt_authentication_python_postgres
COPY scripts/docker-entrypoint.sh scripts/asgi.py scripts/run_tests.sh config.py ./
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
