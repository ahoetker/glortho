#!/usr/bin/env bash
# intended for use with docker-compose.test.yml
# to test outside of Docker, just run `pytest`

echo "Waiting for database to be available"
sleep 5

echo "Performing database migrations"
/venv/bin/alembic upgrade head

echo "Running tests"
/venv/bin/pytest