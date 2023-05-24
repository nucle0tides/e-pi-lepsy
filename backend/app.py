import connexion
import os
from config import DevelopmentCfg
from flask import jsonify, make_response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# NOTE: Always initialize sqlalchemy first and then marshmallow
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def init_app():
    """flask app factory for our flask application

    creates a new instance of our flask app and configures its specific context. this keeps the global namespace clean and prevents circular dependencies which is necessary for our models and schemas.

    for more, see:
    - https://hackersandslackers.com/flask-application-factory/
    - https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/
    """
    cnx_app = connexion.FlaskApp(__name__, specification_dir="./", host="0.0.0.0", port=8080)
    cnx_app.add_api("openapi.yml", pythonic_params=True)

    app = cnx_app.app

    # TODO: have actual config loading logic for env vars, etc
    env_cfg = os.getenv("EPILYPSY_SETTINGS", DevelopmentCfg)
    app.config.from_object(env_cfg)
    DB_PASSWORD = app.config.get('DB_PASSWORD')


    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg://dev:{DB_PASSWORD}@localhost:5433/epilepsy"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # bring our routes into app context
        import api

        # TODO: get rid of this or move it somewhere else
        @app.route("/hi")
        def hi():
            return make_response(jsonify({ "message": "hi from flask" }), 200)

        # import models here for auto-gen migrations
        from models import Household, Pet, SeizureActivity

        return app
