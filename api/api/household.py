from flask import abort, jsonify, make_response
from . import get_timestamp
import uuid

HOUSEHOLDS = {
    1: {
        "id": 1,
        "publicID": "9BE77267-5EC2-4B07-9605-1EF50B64DF5E",
        "createdAt": "2018-07-15T12:00:00.000Z",
        "updatedAt": "2023-04-23T22:47:50.823Z",
        "primaryOwnerName": "Gabby Ortman",
        "primaryOwnerEmail": "ortmangl@gmail.com",
        "secondaryOwnerName": "Elias Garcia",
        "secondaryOwnerEmail": "elias.jm.garcia@gmail.com"
    }
}

ID_ = 1

def read_all():
    return make_response(jsonify(data=list(HOUSEHOLDS.values())), 200)

def create(body):
    global HOUSEHOLDS
    global ID_
    ID_ += 1
    id_ = ID_

    primary_owner_name = body.get("primaryOwnerName")
    primary_owner_email = body.get("primaryOwnerEmail")
    updated_at = created_at = get_timestamp()

    if primary_owner_email and primary_owner_name:
        HOUSEHOLDS[id_] = {
            "id": id_,
            "publicID": uuid.uuid4(),
            "createdAt": created_at,
            "updatedAt": updated_at,
            "primaryOwnerName": primary_owner_name,
            "primaryOwnerEmail": primary_owner_email
        }
        return 201, { "data" : HOUSEHOLDS[id_] }
    
def update(id_, household):
    if id_ in HOUSEHOLDS:
        curr = HOUSEHOLDS[id_]
        primary_owner_name = household.get("primaryOwnerName", curr.get("primaryOwnerName"))
        primary_owner_email = household.get("primaryOwnerEmail", curr.get("primaryOwnerEmail"))
        secondary_owner_name = household.get("secondaryOwnerName", curr.get("secondaryOwnerName"))
        secondary_owner_email = household.get("secondaryOwnerEmail", curr.get("secondaryOwnerEmail"))
        HOUSEHOLDS[id_].update({
            "primaryOwnerName": primary_owner_name,
            "primaryOwnerEmail": primary_owner_email,
            "secondaryOwnerName": secondary_owner_name,
            "secondaryOwnerEmail": secondary_owner_email,
            "updatedAt": get_timestamp()
        })
        return make_response(jsonify(HOUSEHOLDS[id_]), 200)
    else:
        abort(404, f"Household with ID {id_} not found.")

def get(id_):
    if id_ in HOUSEHOLDS:
        return 200, { "data" : HOUSEHOLDS[id_] }
    else:
        abort(404, f"Could not find household with ID: {id_}")

def delete(id_):
    if id_ in HOUSEHOLDS:
        del HOUSEHOLDS[id_]
        return make_response(f"Household with ID {id_} successfully deleted.")
    else:
        abort(404, f"Household with ID {id_} not found.")