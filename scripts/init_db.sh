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
    echo >&2 "With a properly configured dev venv environment, use poetry as follows:"
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


>&2 echo "Postgres is up and running on port ${DB_PORT}"

# TODO: automatically configure to use desired extensions, ie uuid-osp for uuid_generate_v4(), would be very nice.
#       This is a rough outline of what that might look like but I need to test it and then re-write the Flask-Sqlalchemy models to use via server_default=text("uuid_generate_v4()")
# >&2 echo "Setting up PostgreSQL extensions required by application..."

# if ! [[ $(psql -h "localhost" -U "${DB_USER}" -p "${DB_PORT}" -d "${DB_NAME}" -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')]];
# then
#     echo >&2 "extensions failed to install. manual intervention required!"
#     exit 1;
# fi

>&2 echo "Running DB migrations..."

DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}
export DATABASE_URL

FLASK_APP="${FLASK_APP:=run.py}"
export FLASK_APP

cd backend/

poetry run flask db upgrade

>&2 echo "Postgres has been migrated, ready to go!"