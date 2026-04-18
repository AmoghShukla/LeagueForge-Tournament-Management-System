from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.core.config import settings
import src.model  # noqa: F401

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
