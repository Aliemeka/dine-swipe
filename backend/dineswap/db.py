import os

from sqlmodel import SQLModel, create_engine

engine = create_engine(os.getenv("DATABASE_URL", ""))


def create_db_tables():
    SQLModel.metadata.create_all(engine)
