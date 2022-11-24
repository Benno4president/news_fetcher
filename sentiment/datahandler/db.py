import os
from sqlmodel import Session, create_engine, SQLModel
from . import models # preload all models before db creation
from loguru import logger

def get_paths(): # move to main utils. then transform SentimentInterface to something which takes an init
    BASE = os.path.join(os.path.dirname(__file__),'..')
    out = {
        'BASE':BASE,
        'DB':os.path.join(BASE, '..', 'database.db')
    }
    return out

__sqlite_file_name = get_paths()['DB']
_sqlite_url = f"sqlite:///{__sqlite_file_name}"


def get_engine(path_to_db=None, echo=False):
    # just a driver, does not create.
    print('creating engine', path_to_db)
    p = path_to_db if path_to_db else _sqlite_url
    logger.info('Using DB at {}', p)
    engine = create_engine(p, echo=echo)
    return engine

def create_db(init_db_path:_sqlite_url):
    SQLModel.metadata.create_all(get_engine(init_db_path, echo=True))
    print('db creation run')
