from app import db
from flask import abort, jsonify, make_response
from models import Pet, pet_schema, pets_schema

def read_all():
    pets = Pet.query.all()
    return pets_schema.dump(pets)

def create(pet):
    print(pet)
    # TODO: exists check, just like Household
    # TODO: probably want client to be using public_id for households (just as with pets), so should actually look up household by public ID here and then use that
    #       to get the private id for household_id unless we change over to using the public_id for all of it.
    new_pet = Pet(first_name=pet.get("firstName"), last_name=pet.get("lastName"), date_of_birth=pet.get("dateOfBirth"), household_id=pet.get("householdId"))
    db.session.add(new_pet)
    db.session.commit()
    return pet_schema.dump(new_pet)

def update(id_, pet):
    print(f"REQUEST BODY: {pet}")
    curr_pet = Pet.query.filter(Pet.public_id == id_).one_or_none()
    # TODO: try iter with setattr instead of this mess
    # TODO: with pets, should i want some combination of first_name, last_name, household_id, and/or date_of_birth to be a uniqueness constraint? composite key?
    # TODO: Really is an edge case, but what about changing household id's? just disallow it?
    if curr_pet is not None:
        updated_pet = pet_schema.load(pet, partial=True, session=db.session)
        if updated_pet.first_name:
            curr_pet.first_name = updated_pet.first_name
        if updated_pet.last_name:
            curr_pet.last_name = updated_pet.last_name
        if updated_pet.date_of_birth:
            curr_pet.date_of_birth = updated_pet.date_of_birth
        if updated_pet.avatar:
            curr_pet.avatar = updated_pet.avatar
        db.session.merge(curr_pet)
        db.session.commit()
        return pet_schema.dump(curr_pet)
    else:
        abort(404, f"Pet with ID {id_} not found.")

def get(id_):
    pet = Pet.query.filter(Pet.public_id == id_).one_or_none()

    if pet is not None:
        return pet_schema.dump(pet)
    else:
        abort(404, f"Could not find Pet with ID: {id_}")

def delete(id_):
    pet = Pet.query.filter(Pet.public_id == id_).one_or_none()

    if pet is not None:
        db.session.delete(pet)
        db.session.commit()
        return make_response(jsonify({"detail": f"Pet with ID {id_} successfully deleted.", "status": 200}), 200)
    else:
        abort(404, f"Could not find Pet with ID: {id_}")
