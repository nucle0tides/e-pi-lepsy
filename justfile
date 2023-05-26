# tbh it might be better to rely on dotenv support than juggling env values
export FLASK_APP := "run.py"

default:
  just --list

dev-frontend:
    cd frontend && npm run dev

dev-backend:
    cd backend && poetry run flask run --debug --port 8080 --host "0.0.0.0"

# We're assuming NPM and poetry are installed (along with eligible versions of node and python)
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

backend-shell:
  cd backend && poetry run flask shell

# TODO: setup dev db command