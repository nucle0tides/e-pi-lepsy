# NOTE: for any future entity with an updated_at column, need to modify the corresponding alembic migration to execute the trigger for each instance as done in migration:
#       api/migrations/versions/c00f3ae959a6_fixed_updated_at_in_models.py
import enum
from app import db, ma
from datetime import datetime, date
import logging
from sqlalchemy import ForeignKey, func, text, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy.exc import NoResultFound

class CRUDMixin(object):
    @classmethod
    def create(cls, schema, session, data):
        new_obj = schema.load(data, partial=True)
        session.add(new_obj)
        return new_obj

    @classmethod
    def read(cls, session, id_=None, public_id=None):
        logging.info(f"{cls}.read(id: {id_}, public_id: {public_id})")
        if id_ is None and public_id is None:
            raise ValueError("Expected id_ or public_id to be provided as an argument")
        elif id_:
            logging.debug("looking for record by id...")
            # NOTE: I've changed this query from one_or_none() to one() which immediately raises an exception because
            #       my routes are currently structured to expect an exception. The exception is then propagated into an error response handler.
            #       The other CRUD operations also expect this behavior, which allows the exception to be transparent (i.e. record not found as opposed a failed update operation).
            #       I don't know if this is actually a good design.
            return session.query(cls).filter(cls.id == id_).one()
        else:
            logging.debug("looking for record by public_id")
            return session.query(cls).filter(cls.public_id == public_id).one()

    @classmethod
    def update(cls, schema, session, data, id_=None, public_id=None):
        logging.info(f"{cls}.update(data: {data}, id_: {id_}, public_id: {public_id})")
        if id_ is None and public_id is None:
            raise ValueError("Expected id_ or public_id to be provided as an argument")
        elif id_:
            curr_obj = cls.read(session, id_)
            return schema.load(data, partial=True, instance=curr_obj)
        else:
            curr_obj = cls.read(session, public_id=public_id)
            return schema.load(data, partial=True, instance=curr_obj)

    @classmethod
    def delete(cls, session, id_=None, public_id=None):
        logging.info(f"{cls}.delete(id_: {id_}, public_id: {public_id})")
        if id_ is None and public_id is None:
            raise ValueError("Expected id_ or public_id to be provided as an argument")
        elif id_:
            curr_obj = cls.read(session, id_)
            db.session.delete(curr_obj)
        else:
            curr_obj = cls.read(session, public_id=public_id)
            db.session.delete(curr_obj)


class SeizureType(enum.Enum):
    TONICCLONIC = "tonic-clonic"
    FOCAL = "focal"
    UNSPECIFIED = "unspecified"

class Pet(db.Model, CRUDMixin):
    __tablename__ = "pet"
    __table_args__ = (UniqueConstraint("public_id"), UniqueConstraint("first_name", "last_name", "household_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    household_id: Mapped[UUID] = mapped_column(ForeignKey("household.public_id"))
    date_of_birth: Mapped[date] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[Optional[str]] = mapped_column()
    avatar: Mapped[Optional[str]] = mapped_column()

    household: Mapped["Household"] = relationship(back_populates="pets")
    seizures: Mapped[List["SeizureActivity"]] = relationship(back_populates="pet")

class Household(db.Model, CRUDMixin):
    __tablename__ = "household"
    __table_args__ = (UniqueConstraint("public_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    # NOTE: I would like to use uuid_generate_v4() instead but i'm tired of dealing with alembic and sqlalchemy lol
    public_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    primary_owner_name: Mapped[str] = mapped_column()
    primary_owner_email: Mapped[str] = mapped_column(unique=True)
    secondary_owner_name: Mapped[Optional[str]] = mapped_column()
    secondary_owner_email: Mapped[Optional[str]] = mapped_column()

    # NOTE: should probably update relation to define DELETE ON CASCADE behavior
    pets: Mapped[List["Pet"]] = relationship(back_populates="household")

class SeizureActivity(db.Model, CRUDMixin):
    __tablename__ = "seizure_activity"
    __table_args__ = (UniqueConstraint("public_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    pet_id: Mapped[UUID] = mapped_column(ForeignKey("pet.public_id"))
    date: Mapped[date] = mapped_column(Date)
    # NOTE: might be better to store seizure_start, seizure_end and then have a computed column
    # NOTE: sqlalchemy sucks and i don't care to deal with tracking changes to interior mutability of postgres arrays
    #       so i'm moving ahead with having two columns instead of one
    # alternative 1: create a composite type to represent this on the backend
    # alternative 2: have the duration calculated by the client and then this becomes a Time column
    # as of now, have to respect contract that we only provide two datetimes in the list
    seizure_start: Mapped[Optional[datetime]] = mapped_column()
    seizure_end: Mapped[Optional[datetime]] = mapped_column()
    # NOTE: since SeizureType is an enum, we don't assign it to mapped_column()
    seizure_type: Mapped[SeizureType]
    # NOTE: see seizure_start notes 
    episode_start: Mapped[datetime] = mapped_column()
    episode_end: Mapped[datetime] = mapped_column()
    location: Mapped[Optional[str]] = mapped_column()
    notes: Mapped[Optional[str]] = mapped_column()
    # NOTE: similar problem as seizure_duration lol
    medication_administered: Mapped[Optional[str]] = mapped_column()
    medication_dosage: Mapped[Optional[str]] = mapped_column()

    pet: Mapped["Pet"] = relationship(back_populates="seizures")

def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)

class CamelCaseSchema(ma.Schema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

class HouseholdSchema(ma.SQLAlchemyAutoSchema, CamelCaseSchema):
    class Meta:
        model = Household
        load_instance = True
        sqla_session = db.session
        exclude = ("id", "created_at", "updated_at")


household_schema = HouseholdSchema()
households_schema = HouseholdSchema(many=True)

class PetSchema(ma.SQLAlchemyAutoSchema, CamelCaseSchema):
    class Meta:
        model = Pet
        load_instance = True
        sqla_session = db.session
        include_fk = True
        exclude = ("id", "created_at", "updated_at")

pet_schema = PetSchema()
pets_schema = PetSchema(many=True)

class SeizureActivitySchema(ma.SQLAlchemyAutoSchema, CamelCaseSchema):
    class Meta:
        model = SeizureActivity
        load_instance = True
        sqla_session = db.session
        include_fk = True
        exclude = ("id", "created_at", "updated_at")

seizure_activity_schema = SeizureActivitySchema()
seizure_activities_schema = SeizureActivitySchema(many=True)
