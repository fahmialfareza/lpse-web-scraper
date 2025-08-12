from sqlalchemy import create_engine, inspect
from config.config import LPSE_POSTGRES_URL
from db.tender_model import Base

# Create the database engine
engine = create_engine(LPSE_POSTGRES_URL)

# Create the database tables
Base.metadata.create_all(engine)

insp = inspect(engine)
print("Has tender?", insp.has_table("tender", schema="public"))
