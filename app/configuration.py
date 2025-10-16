import os
from .scrapers import active_scrapers

class Configuration:
    db_path:str = os.getenv("DATABASE")
    partitioned_scrapers:dict = os.getenv("SCRAPERS", "all")
