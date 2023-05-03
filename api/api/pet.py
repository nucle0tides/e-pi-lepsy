from . import get_timestamp
from flask import abort, jsonify, make_response
import uuid



PETS = {
    "smalls": {
        "id": 1,
        "publicID": "695F20B9-C89A-4F56-B1DD-F01CF6AC9279",
        "createdAt": "2023-04-23T22:41:30.299Z",
        "updatedAt": "2023-04-23T22:41:30.299Z",
        "householdId": 1,
        "firstName": "Biggie Smalls",
        "lastName": "Ortman",
        "dateOfBirth": "2010-08-13T12:00:00.000Z",
        "avatar": "30298cb1ce4c9f140718a3930122faa6.jpg"
    },
    "pius": {
        "id": 2,
        "publicID": "47726D96-D9AE-43C1-A5ED-7835CC6AC558",
        "createdAt": "2023-04-23T22:41:30.299Z",
        "updatedAt": "2023-04-23T22:41:30.299Z",
        "householdId": 1,
        "firstName": "Antoninus Pius",
        "lastName":  "Ortman",
        "dateOfBirth": "2018-07-15T12:00:00.000Z",
        "avatar": "1fc3912f639283b14bcd750d3d955605.jpg"
    }
}

ID_ = 2

def read_all():
    return { "data": list(PETS.values()) }

def create(pet):
    print(pet)
    last_name = pet.get("lastName")
    first_name = pet.get("firstName")
    date_of_birth = pet.get("dateOfBirth")
    household_id = pet.get("householdId")
    createdAt = updatedAt = get_timestamp()
    global ID_
    ID_ += 1
    id_ = ID_
    global PETS
    if first_name and first_name not in PETS:
        PETS[first_name] = {
            "id": id_,
            "publicId": uuid.uuid4(),
            "createdAt": createdAt,
            "updatedAt": updatedAt,
            "householdId": household_id,
            "firstName": first_name,
            "lastName": last_name,
            "dateOfBirth": date_of_birth
        }
        return PETS[first_name], 201

def update(id_, pet):
    for pet_ in PETS:
        if PETS[pet_]["id"] == id_: 
            curr = PETS[pet_]
            household_id = pet.get("householdId", curr.get("householdId"))
            first_name = pet.get("firstName", curr.get("firstName"))
            last_name = pet.get("lastName", curr.get("lastName"))
            date_of_birth = pet.get("dateOfBirth", curr.get("dateOfBirth"))
            PETS[pet_].update({
                "householdId": household_id,
                "firstName": first_name,
                "lastName": last_name,
                "dateOfBirth": date_of_birth,
                "updatedAt": get_timestamp()
            })
            return make_response(jsonify(PETS[pet_]), 200)
    abort(404, f"Pet with ID {id_} not found.")

def get(id_):
    for pet in PETS:
        if PETS[pet]["id"] == id_:
            return 200, {"data": PETS[pet]}
    abort(404, f"Could not find Pet with ID: {id_}")

def delete(id_):
    for pet in PETS:
        if PETS[pet]["id"] == id_:
            del PETS[pet]
            return make_response(f"Pet with ID {id_} successfully deleted.", 200)
    abort(404, f"Pet with ID {id_} not found.")