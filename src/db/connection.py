from sqlalchemy import create_engine
from config.config import LPSE_POSTGRES_URL

# Create the database engine
engine = create_engine(LPSE_POSTGRES_URL)
