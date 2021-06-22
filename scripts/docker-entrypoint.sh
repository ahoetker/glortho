#!/usr/bin/env bash

echo "Performing database migrations"
/venv/bin/alembic upgrade head

PORT="${PORT:-8080}"
echo "Starting app at ${PORT}"
exec /venv/bin/gunicorn -c config.py asgi:app