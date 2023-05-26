from app import db
from flask import abort, jsonify, make_response
from models import Household, household_schema, households_schema
from sqlalchemy import exc 

def read_all():
    households = Household.query.all()
    return households_schema.dump(households)

def create(body):
    try:
        new_household = Household.create(schema=household_schema, session=db.session, data=body)
        db.session.commit()
        return household_schema.dump(new_household)
    except exc.SQLAlchemyError:
        abort(404, f"Could not create household.")
    
def update(id_, household):
    try:
        updated_household = Household.update(schema=household_schema, session=db.session, data=household, public_id=id_)
        db.session.commit()
        return household_schema.dump(updated_household)
    except exc.SQLAlchemyError:
        abort(404, f"Could not update household")

def get(id_):
    try:
        household = Household.read(session=db.session, public_id=id_)
        return household_schema.dump(household)
    except exc.SQLAlchemyError:
        abort(404, f"Could not find household with ID: {id_}")

def delete(id_):
    try:
        Household.delete(session=db.session, public_id=id_)
        db.session.commit()
        return make_response(jsonify({"detail": f"Household with ID {id_} successfully deleted", "status": 200}), 200)
    except exc.SQLAlchemyError:
        abort(404, f"Household with ID {id_} not found.")