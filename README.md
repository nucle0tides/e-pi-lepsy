# e-pi-lepsy
latest and greatest iteration of managing, tracking, and visualizing my chronically ill dog's health

## development

Dev tool requirements:
- modern version of node (>= v18)
- python (>=3.11)
    - [pyenv](https://github.com/pyenv/pyenv) is very good for handling python versions but is not necessary for the project.
- npm
- [poetry](https://github.com/python-poetry/install.python-poetry.org)
  - Poetry is used for also handling the virtualenv setup for the project. While not strictly necessary, allowing Poetry to directly manage the virtualenv simplifies things (as opposed to making virtualenv management a part of the workflow i.e. `pyenv-virtualenv`).
- modern version of docker
- modern version of PostgreSQL (>=v14 should be OK)
- [just](https://github.com/casey/just)
    - optional, only necessary if you'd like to use the provided [justfile](justfile) for development.
    - if not using `just`, look at the provided [`justfile`](justfile) for the commands necessary to build and run the application as the install instructions below will not be valid.
    - In particular, pay attention to how the python backend is installed/ran along with the DB setup.

### installing and setup

Assuming you have the following tools installed and on your `PATH`, from the project root you can run:
```
just dev-install
```
and the project dependencies for both the `frontend` and `backend` will be installed along with setting up the DB, running all migrations, and seeding it with dummy data.

After that, run `dev-backend` and `dev-frontend` in separate shells for a fully running application or separately as necessary for development. You should be able to open http://localhost:3000 for the client and send HTTP requests to the backend at http://localhost:8080.

### issues setting up

If using vscode: IME you will have to change the setting "Default Interpreter Path" for the workspace to `${workspaceFolder}/backend/.venv/bin/python` in order for vscode to see and use the proper virtualenv. A workspace settings file has been provided in the repo with that configuration already set.

Docker expects port 5433 to be available on your side of things; if something is already binded, you will need to change that in the [init_db.sh](scripts/init_db.sh) script.