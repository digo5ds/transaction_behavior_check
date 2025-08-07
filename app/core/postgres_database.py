"""PostgreSQL database factory."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import (
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTIGRES_HOST,
)

DATABASE_URL = (
    "postgresql+psycopg2://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTIGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency to get a database session.

    This function is a generator that will create a new database session
    for each request, and automatically close it when the request is finished.

    This is the recommended way to share a database session between multiple
    parts of a request, such as between endpoint functions and their dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
