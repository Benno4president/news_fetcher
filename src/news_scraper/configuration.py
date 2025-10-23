import os
import json
from loguru import logger
from scrapers import active_scrapers

class Configuration:
    db_path:str = os.getenv("DATABASE_URL")
    partitioned_scrapers:dict = json.loads(os.getenv("SCRAPERS", '["all"]'))
    interval_time_minutes = os.getenv("INTERVAL_TIME_MINUTE", "0")


logger.info(
    "News Scraper Configuration loaded: {}", 
    {k:v for k,v in Configuration.__dict__.items() if not k.startswith('__')}
    )