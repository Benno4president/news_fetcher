import os
from sqlmodel import Session, create_engine, SQLModel
from mother.constants import DATABASE_DEBUG, BASE_PATH
from . import models # preload all models before db creation

__sqlite_file_name = os.path.join(BASE_PATH,"database.db")
__sqlite_url = f"sqlite:///{__sqlite_file_name}"

# just a driver, does not create.
engine = create_engine(__sqlite_url, echo=DATABASE_DEBUG)


def create_db():
    SQLModel.metadata.create_all(engine)
    print('db creation run')
