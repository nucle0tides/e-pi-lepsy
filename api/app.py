import connexion
import os
from config import DevelopmentCfg
from flask import jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

cnx_app = connexion.FlaskApp(__name__, specification_dir="../", host="0.0.0.0", port=8080)
cnx_app.add_api("openapi.yml", pythonic_params=True)

app = cnx_app.app

# TODO: have actual config loading logic for env vars, etc
env_cfg = os.getenv("EPILYPSY_SETTINGS", DevelopmentCfg)
app.config.from_object(env_cfg)
DB_PASSWORD = app.config.get('DB_PASSWORD')


app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg://dev:{DB_PASSWORD}@localhost:5433/epilepsy"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Have to import my models here for autogeneration in migrations
from models import SeizureType, Household, Pet, SeizureActivity

@app.route("/hi")
def hi():
    return make_response(jsonify({ "message": "hi from flask" }), 200)
