from typing import List
import pandas as pd
from .db import Session, get_engine
from sqlmodel import select
from .models import ScraperResult

class ToolDBInterface:
    def __init__(self, db_path=None) -> None:
        self.db_path = db_path
        self.engine = get_engine(db_path)

    def get_published_dates(self):
        # get dates in db
        with Session(self.engine) as sess:
            statement = select(ScraperResult.published)
            res = sess.exec(statement).all()
        return res
    
    def get_all_by_date(self, dates:List[str]):
        with Session(self.engine) as sess:
            statement = select(ScraperResult).where(ScraperResult.published.in_(dates))
            res = sess.exec(statement).all()
        return res
    
    def get_all_text(self):
        with Session(self.engine) as sess:
            statement = select(ScraperResult.text)
            res = sess.exec(statement).all()
            return res