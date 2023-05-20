from app import db
from flask import abort, jsonify, make_response
from models import Household, household_schema, households_schema
# from . import get_timestamp
# import uuid

def read_all():
    households = Household.query.all()
    return households_schema.dump(households)

def create(body):
    # TODO: connexion provides me some guarantees via openAPI spec (request must have JSON body with primaryOwnerName, etc) but there are probably some other things i should check here before
    #       committing to the database, i.e.
    #           household = Household.query.filter(Household.primary_owner_email == body.get("primaryOwnerEmail")).first()
    #           if household is not None:
    #           // etc
    #           else:
    new_household = Household(primary_owner_name=body.get("primaryOwnerName"), primary_owner_email=body.get("primaryOwnerEmail"), secondary_owner_name=body.get("secondaryOwnerName"), secondary_owner_email=body.get("secondaryOwnerEmail"))
    db.session.add(new_household)
    db.session.commit()
    return household_schema.dump(new_household)
    
def update(id_, household):
    print(f"REQUEST BODY: {household}")
    curr_household = Household.query.filter(Household.public_id == id_).one_or_none()

    # TODO: try iter with setattr instead of this mess
    # TODO: how to best check for uniqueness over column vals with uniqueness constraints & handling that
    if curr_household is not None:
        updated_household = household_schema.load(household, partial=True, session=db.session)
        if updated_household.primary_owner_name:
            curr_household.primary_owner_name = updated_household.primary_owner_name
        if updated_household.primary_owner_email:
            curr_household.primary_owner_email = updated_household.primary_owner_email
        if updated_household.secondary_owner_name:
            curr_household.secondary_owner_name = updated_household.secondary_owner_name
        if updated_household.secondary_owner_email:
            curr_household.secondary_owner_email = updated_household.secondary_owner_email
        db.session.merge(curr_household)
        db.session.commit()
        return household_schema.dump(curr_household)
    else:
        abort(404, f"Household with ID {id_} not found.")

def get(id_):
    household = Household.query.filter(Household.public_id == id_).one_or_none()

    if household is not None:
        return household_schema.dump(household)
    else:
        abort(404, f"Could not find household with ID: {id_}")

def delete(id_):
    household = Household.query.filter(Household.public_id == id_).one_or_none()

    if household:
        db.session.delete(household)
        db.session.commit()
        return make_response(jsonify({"detail": f"Household with ID {id_} successfully deleted", "status": 200}), 200)
    else:
        abort(404, f"Household with ID {id_} not found.")