from app import db
from flask import abort, jsonify, make_response
from models import Pet, pet_schema, pets_schema
from sqlalchemy import exc

def read_all():
    pets = Pet.query.all()
    return pets_schema.dump(pets)

def create(pet):
    try:
        new_pet = Pet.create(schema=pet_schema, session=db.session, data=pet)
        db.session.commit()
        return pet_schema.dump(new_pet)
    except exc.SQLAlchemyError:
        abort(404, "Could not create pet.")

def update(id_, pet):
    try:
        updated_pet = Pet.update(schema=pet_schema, session=db.session, data=pet, public_id=id_)
        db.session.commit()
        return pet_schema.dump(updated_pet)
    except exc.SQLAlchemyError:
        abort(404, f"Could not update pet with ID: {id_}")

def get(id_):
    try:
        pet = Pet.read(session=db.session, public_id=id_)
        return pet_schema.dump(pet)
    except exc.SQLAlchemyError:
        abort(404, f"Could not find pet with ID: {id_}")

def delete(id_):
    try:
        Pet.delete(session=db.session, public_id=id_)
        db.session.commit()
        return make_response(jsonify({"detail": f"Pet with ID {id_} successfully deleted.", "status": 200}), 200)
    except exc.SQLAlchemyError:
        abort(404, f"Could not find Pet with ID: {id_}")
