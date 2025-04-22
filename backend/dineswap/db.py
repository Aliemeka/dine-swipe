import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

engine = create_engine(os.getenv("DATABASE_URL", ""), echo=True)

session = sessionmaker(engine)

def create_db_tables():
    SQLModel.metadata.create_all(engine)
