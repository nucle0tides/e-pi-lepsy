"""Initialize database with dummy data"""

# TODO: clean up import structure. This works but it should probably be less messy?
from models import Household, Pet
from app import db
from run import app

HOUSEHOLDS_WITH_PETS = [
    {
        "primary_owner_name": "Gabby Ortman",
        "primary_owner_email": "made-up-email-1@gmail.com",
        "secondary_owner_name": "Elias Garcia",
        "secondary_owner_email": "elias.jm.garcia@gmail.com",
        "pets": [
            {
                "first_name": "Biggie Smalls",
                "last_name": "Ortman",
                "date_of_birth": "2010-08-13T12:00:00.000Z",
                "avatar": "30298cb1ce4c9f140718a3930122faa6.jpg"
            },
            {
                "first_name": "Antoninus Pius",
                "last_name":  "Ortman",
                "date_of_birth": "2018-07-15T12:00:00.000Z",
                "avatar": "1fc3912f639283b14bcd750d3d955605.jpg"
            }
        ]
    },
    {
        "primary_owner_name": "AG",
        "primary_owner_email": "made-up-email-2@gmail.com",
        "secondary_owner_name": "AVGM",
        "secondary_owner_email": "made-up-email-3@gmail.com",
        "pets": [
            {
                "first_name": "Zinc",
                "last_name":  "Garcia",
                "date_of_birth": "2011-09-10T12:00:00.000Z",
                "avatar": "6992f47ebb82aa68353413e5b78ce8c6.jpg"
            },
            {
                "first_name": "Gandalf",
                "last_name":  "Garcia",
                "date_of_birth": "2013-08-05T12:00:00.000Z",
                "avatar": "1b17e0fee3ef12f44446fd344011e38a.jpg"
            },
            {
                "first_name": "Luna Leia",
                "last_name":  "Garcia",
                "date_of_birth": "2014-04-09T12:00:00.000Z",
                "avatar": "6f16e10c2117b99bd894138d6f1f06ab.jpg"
            },
            {
                "first_name": "Axel",
                "last_name":  "Garcia",
                "date_of_birth": "2015-10-03T12:00:00.000Z",
                "avatar": "3d3fb7a9b60a8aaafb92d538a0cdefe6.jpg"
            },
            {
                "first_name": "Braveheart",
                "last_name":  "Garcia",
                "date_of_birth": "2016-02-11T12:00:00.000Z",
                "avatar": "3683e8576847de81b8a9956c99229626.jpg"
            },            
        ]
    }
]

with app.app_context():
    db.drop_all()
    db.create_all()

    for household in HOUSEHOLDS_WITH_PETS:
        new_household = Household(primary_owner_name=household.get("primary_owner_name"), primary_owner_email=household.get("primary_owner_email"), secondary_owner_name=household.get("secondary_owner_name"), secondary_owner_email=household.get("secondary_owner_email"))

        for pet in household.get("pets"):
            new_household.pets.append(Pet(
                first_name=pet.get("first_name"),
                last_name=pet.get("last_name"),
                date_of_birth=pet.get("date_of_birth")
                )
            )
        db.session.add(new_household)
    db.session.commit()