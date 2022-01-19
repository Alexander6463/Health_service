import os

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL", default="postgresql+psycopg2://postgres:4014@localhost:5432/test_2"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
