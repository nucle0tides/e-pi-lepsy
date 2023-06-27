from app import db
from flask import abort, jsonify, make_response
from models import Pet, pet_schema, pets_schema
from sqlalchemy import exc

def read_all(p_id):
    return "pet.seizure.read_all", 200

def update(p_id, s_id):
    return "pet.seizure.update", 200

def create(p_id):
    return "pet.seizure.create", 200

def delete(p_id, s_id):
    return "pet.seizure.delete", 200

def get(p_id, s_id):
    return "pet.seizure.get", 200