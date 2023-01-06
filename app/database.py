from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"mysql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

# Establishes connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Makes a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Used to create each of the database models or classes (the ORM models)
Base = declarative_base()

# Establishes connection with the database
def get_db():
    # Instance of SessionLocal -> Database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()