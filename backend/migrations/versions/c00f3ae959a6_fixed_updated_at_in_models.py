"""fixed updated_at in models

Revision ID: c00f3ae959a6
Revises: 23a4ebe43ed5
Create Date: 2023-05-20 15:10:19.131310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c00f3ae959a6'
down_revision = '23a4ebe43ed5'
branch_labels = None
depends_on = None

ON_UPDATE_POSTGRESQL_TRIGGER_DECLARATION = """
create or replace function set_updated_at()
    returns trigger as
$$
begin
    NEW.updated_at = now();
    return NEW;
end;
$$ language plpgsql;

create or replace function trigger_updated_at(tablename regclass)
    returns void as
$$
begin
    execute format('CREATE TRIGGER set_updated_at
        BEFORE UPDATE
        ON %s
        FOR EACH ROW
        WHEN (OLD is distinct from NEW)
    EXECUTE FUNCTION set_updated_at();', tablename);
end;
$$ language plpgsql;
"""

def upgrade():
    op.execute(sa.text(ON_UPDATE_POSTGRESQL_TRIGGER_DECLARATION))
    for table in ['household', 'pet', 'seizure_activity']:
        op.execute(f"SELECT trigger_updated_at('{table}');")

def downgrade():
    for table in ['household', 'pet', 'seizure_activity']:
        op.execute(f"DROP TRIGGER IF EXISTS  trigger_updated_at ON {table};")
    op.execute("DROP FUNCTION IF EXISTS trigger_updated_at;")
    op.execute("DROP FUNCTION IF EXISTS set_updated_at;")