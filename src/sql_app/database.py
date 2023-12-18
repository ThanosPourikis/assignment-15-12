import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = (
    f'sqlite:///{os.environ.get("DATA_FOLDER", "data")}/sqlite.db'
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db_conxt() -> Session:
    """
    Simple context manager

    :return: Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db() -> Session:
    """
    Generator for fastapi connection
    :return: Generator[Session]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
