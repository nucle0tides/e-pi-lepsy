#!/usr/bin/env bash
set -x
set -eo pipefail

# check for psql
if ! [ -x "$(command -v psql)" ]; then
    echo >&2 "Error: psql is not installed."
    exit 1
fi

#check for python version? sqlalchemy? alembic?
if ! [ -x "$(command -v flask)" ]; then
    echo >&2 "Error: flask is not installed"
    echo >&2 "Install with poetry and within the correct venv environment."
    echo >&2 "    poetry add flask Flask-Migrate && poetry shell"
    exit 1
fi

# Check if a custom user has been set, otherwise default to 'dev'
DB_USER="${POSTGRES_USER:=dev}"
# Check if a custom password has been set, otherwise default to 'password'
DB_PASSWORD="${POSTGRES_PASSWORD:=password}"
# Check if a custom database name has been set, otherwise default to 'epilepsy'
DB_NAME="${POSTGRES_DB:=epilepsy}"
# Check if a custom port has been set, otherwise default to '5433'
DB_PORT="${POSTGRES_PORT:=5433}"

# Allow to skip Docker if a dockerized Postgres database is already running
if [[ -z "${SKIP_DOCKER}" ]]
then
    # Launch postgres using Docker
    docker run \
        -e POSTGRES_USER=${DB_USER} \
        -e POSTGRES_PASSWORD=${DB_PASSWORD} \
        -e POSTGRES_DB=${DB_NAME} \
        -p "${DB_PORT}":5432 \
        -d postgres \
        postgres -N 100 
    # connections
fi

# Keep pinging Postgres until it's ready to accept commands
export PGPASSWORD="${DB_PASSWORD}"

until psql -h "localhost" -U "${DB_USER}" -p "${DB_PORT}" -d "${DB_NAME}" -c '\q'; do
    >&2 echo "Postgres is still unavailable - sleeping"
    sleep 1 
done

# TODO? migrations etc
>&2 echo "Postgres is up and running on port ${DB_PORT}"
>&2 echo "WARN: Migrations currently not automated."

# DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}
# export DATABASE_URL

# FLASK_APP="${FLASK_APP:=app.py}"
# export FLASK_APP

# poetry run flask db init

# >&2 echo "Postgres has been migrated, ready to go!"