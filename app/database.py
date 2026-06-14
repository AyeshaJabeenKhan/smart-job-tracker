from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_tracker.db")

# 1. Create the Database Engine
# 'connect_args' configuration is specific to SQLite to allow multi-threaded access
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# 2. Create a Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create the Declarative Base class for ORM Mapping
Base = declarative_base()

# 4. Dependency Injection Function for Database Sessions
def get_db() -> Generator:
    """
    Dependency generator that yields a database session per request.
    Ensures that the session connection is closed automatically after
    the HTTP request lifecycle is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()