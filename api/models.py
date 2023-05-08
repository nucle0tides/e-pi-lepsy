import enum
from app import db, ma
from datetime import datetime, date
from sqlalchemy import ForeignKey, func, text, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

# class DbMetaBase(DeclarativeBase):
#     pass

class SeizureType(enum.Enum):
    TONICCLONIC = "tonic-clonic"
    FOCAL = "focal"
    UNSPECIFIED = "unspecified"

class Pet(db.Model):
    __tablename__ = "pet"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())
    household_id: Mapped[int] = mapped_column(ForeignKey("household.id"))
    date_of_birth: Mapped[date] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[Optional[str]] = mapped_column()

    household: Mapped["Household"] = relationship(back_populates="pets")

class Household(db.Model):
    __tablename__ = "household"

    id: Mapped[int] = mapped_column(primary_key=True)
    # NOTE: I would like to use uuid_generate_v4() instead but i'm tired of dealing with alembic and sqlalchemy lol
    public_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())
    primary_owner_name: Mapped[str] = mapped_column()
    primary_owner_email: Mapped[str] = mapped_column()
    secondary_owner_name: Mapped[Optional[str]] = mapped_column()
    secondary_owner_email: Mapped[Optional[str]] = mapped_column()

    pets: Mapped[List["Pet"]] = relationship(back_populates="household")

class HouseholdSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Household
        load_instance = True
        sqla_session = db.session


household_schema = HouseholdSchema()
households_schema = HouseholdSchema(many=True)

class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        load_instance = True
        sqla_session = db.session
        include_fk = True

pet_schema = PetSchema()
pets_schema = PetSchema(many=True)


class SeizureActivity(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())
    pet_id: Mapped[int] = mapped_column(ForeignKey("pet.id"))
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

class SeizureActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SeizureActivity
        load_instance = True
        sqla_session = db.session
        include_fk = True

seizure_activity_schema = SeizureActivitySchema()
seizure_activities_schema = SeizureActivitySchema(many=True)
