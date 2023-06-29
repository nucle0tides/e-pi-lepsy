from app import db
from flask import abort, jsonify, make_response
from models import Pet, pet_schema, pets_schema, SeizureActivity, seizure_activities_schema, seizure_activity_schema
from sqlalchemy import exc

def read_all(p_id):
    try:
        pet = Pet.read(session=db.session, public_id=p_id)
        return seizure_activities_schema.dump(pet.seizures)
    except exc.NoResultFound:
        abort(404, f"Could not find pet with ID: {p_id}")
    except exc.SQLAlchemyError:
        abort(400, "Bad request.")

def create(p_id, activity):
    try:
        # This read query isn't really necessary but it might be a useful pattern for better error messaging, ie NoRecordFound vs IntegrityError.
        Pet.read(db.session, public_id=p_id)
        new_activity = SeizureActivity.create(schema=seizure_activity_schema, session=db.session, data=activity)
        db.session.commit()
        return seizure_activity_schema.dump(new_activity)
    except exc.NoResultFound:
        abort(404, f"Could not find pet with ID: {p_id}")
    except exc.IntegrityError:
        abort(400, f"Request data invalid, could not create new seizure activity.")
    except exc.SQLAlchemyError:
        abort(404, "Could not create seizure activity log.")

def update(p_id, s_id, activity):
    try:
        Pet.read(session=db.session, public_id=p_id)
        updated_activity = SeizureActivity.update(schema=seizure_activity_schema, session=db.session, data=activity, public_id=s_id)
        db.session.commit()
        return seizure_activity_schema.dump(updated_activity)
    except exc.NoResultFound:
        abort(404, f"Unable to find resource with IDs.")
    except exc.IntegrityError:
        abort(400, f"Request data invalid, could not update seizure activity.")
    except exc.SQLAlchemyError:
        abort(404, "Could not update seizure activity.")

def get(p_id, s_id):
    try:
        Pet.read(session=db.session, public_id=p_id)
        activity = SeizureActivity.read(session=db.session, public_id=s_id)
        return seizure_activity_schema.dump(activity)
    except exc.NoResultFound:
        abort(404, f"Unable to find resource with IDs.")
    except exc.IntegrityError:
        abort(400, f"Request data invalid.")
    except exc.SQLAlchemyError:
        abort(404, "Bad request.")

def delete(p_id, s_id):
    try:
        Pet.read(session=db.session, public_id=p_id)
        SeizureActivity.delete(session=db.session, public_id=s_id)
        db.session.commit()
        return make_response(jsonify({"detail": f"Seizure Activity with ID {s_id} successfully deleted.", "status": 200}), 200)
    except exc.NoResultFound:
        abort(404, f"Unable to find resource with IDs.")
    except exc.IntegrityError:
        abort(400, "Request data invalid.")
    except exc.SQLAlchemyError:
        abort(404, "Bad request.")