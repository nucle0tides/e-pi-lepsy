# env variable for Flask application entry point. TODO(?): use just's dot-env integration instead.
export FLASK_APP := "run.py"

default:
  just --list

# Run client in developer mode.
dev-frontend:
    cd frontend && npm run dev

# Run backend in developer mode.
dev-backend:
    cd backend && poetry run flask run --debug --port 8080 --host "0.0.0.0"

# Install development environement for client, backend, and database. 
dev-install:
  @echo "Installing client..."
  cd frontend && npm install
  @echo "Installing backend..."
  # WARNING: IME when using vscode, you will have to change the setting "Default Interpreter Path" for the workspace to `${workspaceFolder}/backend/.venv/bin/python` in order for vscode to see and use the proper virtualenv.
  cd backend && poetry config virtualenvs.in-project true && poetry install
  @echo "Setting up Dockerized PostgreSQL and running DB migrations..."
  chmod +x scripts/init_db.sh && ./scripts/init_db.sh
  @echo "Seeding database..."
  cd backend && poetry run python init_db.py

# Open shell into backend session within the flask environment.
backend-shell:
  cd backend && poetry run flask shell

# create a new migration with MESSAGE in quotes, ex: just db-migrate 'added new column foobar'.
db-migrate MESSAGE:
  cd backend && poetry run flask db migrate -m "{{MESSAGE}}"

# check for any changes to DB schema that haven't been given a migration.
db-check:
  cd backend && poetry run flask db check

# run any un-applied migrations to DB.
db-upgrade:
  cd backend && poetry run flask db upgrade

# revert DB to previous migration.
db-downgrade:
  cd backend && poetry run flask db downgrade