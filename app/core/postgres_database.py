"""PostgreSQL database factory."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

DATABASE_URL = (
    "postgresql+psycopg2://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db():
    """
    Dependency to get a database session.

    Yields a database session for use in FastAPI path operation functions.
    Closes the session when the context is exited.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
