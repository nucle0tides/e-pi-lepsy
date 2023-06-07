"""fixed referenced FK constraints (id -> public_id)

Revision ID: fddf61f696c5
Revises: c00f3ae959a6
Create Date: 2023-06-07 13:28:39.999032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fddf61f696c5'
down_revision = 'c00f3ae959a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    with op.batch_alter_table('household', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_household_primary_owner_email'), ['primary_owner_email'])
        batch_op.create_unique_constraint(batch_op.f('uq_household_public_id'), ['public_id'])

    # I don't fully understand why creating a column in a batch operation is incompatible with executing data transactions against that new column but here we are.
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('household_id_', sa.UUID(), nullable=True))

    session.execute(sa.text("UPDATE pet SET household_id_ = household.public_id FROM household WHERE pet.household_id=household.id"))

    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.drop_constraint('pet_household_id_fkey', type_='foreignkey')
        batch_op.drop_column('household_id')
        batch_op.alter_column('household_id_', new_column_name="household_id", existing_nullable=True, nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_pet_first_name'), ['first_name', 'last_name', 'household_id'])
        batch_op.create_unique_constraint(batch_op.f('uq_pet_public_id'), ['public_id'])
        batch_op.create_foreign_key(batch_op.f('fk_pet_household_id_household'), 'household', ['household_id'], ['public_id'])

    with op.batch_alter_table('seizure_activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pet_id_', sa.UUID(), nullable=True))

    session.execute(sa.text("UPDATE seizure_activity SET pet_id_ = pet.public_id FROM pet WHERE seizure_activity.pet_id=pet.id"))

    with op.batch_alter_table('seizure_activity', schema=None) as batch_op:
        batch_op.drop_constraint('seizure_activity_pet_id_fkey', type_='foreignkey')
        batch_op.drop_column('pet_id')
        batch_op.alter_column('pet_id_', new_column_name='pet_id', existing_nullable=True, nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_seizure_activity_public_id'), ['public_id'])
        batch_op.create_foreign_key(batch_op.f('fk_seizure_activity_pet_id_pet'), 'pet', ['pet_id'], ['public_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    with op.batch_alter_table('seizure_activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pet_id_', sa.Integer(), nullable=True))

    session.execute(sa.text("UPDATE seizure_activity SET pet_id_ = pet.id FROM pet WHERE seizure_activity.pet_id=pet.public_id"))

    with op.batch_alter_table('seizure_activity', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_seizure_activity_pet_id_pet'), type_='foreignkey')
        batch_op.drop_column('pet_id')
        batch_op.alter_column('pet_id_', new_column_name='pet_id', existing_nullable=True, nullable=False)
        batch_op.create_foreign_key('seizure_activity_pet_id_fkey', 'pet', ['pet_id'], ['id'])
        batch_op.drop_constraint(batch_op.f('uq_seizure_activity_public_id'), type_='unique')

    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('household_id_', sa.Integer(), nullable=True))

    session.execute(sa.text("UPDATE pet SET household_id_ = household.id FROM household WHERE pet.household_id=household.public_id"))

    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_pet_household_id_household'), type_='foreignkey')
        batch_op.drop_column('household_id')
        batch_op.alter_column('household_id_', new_column_name='household_id', existing_nullable=True, nullable=False)
        batch_op.create_foreign_key('pet_household_id_fkey', 'household', ['household_id'], ['id'])
        batch_op.drop_constraint(batch_op.f('uq_pet_public_id'), type_='unique')
        # NOTE: I have literally no idea why this operation throws an 'constraint "uq_pet_first_name" of relation "pet" does not exist' error when the constraint does, in fact, exist.
        #       What is even MORE confusing is that after commenting this out and running the downgrade script, the aforementioned constraint is STILL REMOVED AS IF THIS OP WAS NOT COMMENTED OUT.
        # batch_op.drop_constraint(batch_op.f('uq_pet_first_name'), type_='unique')

    with op.batch_alter_table('household', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_household_public_id'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_household_primary_owner_email'), type_='unique')

    # ### end Alembic commands ###