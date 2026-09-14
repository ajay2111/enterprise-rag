from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Applicant, Base

from app.config import settings

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


