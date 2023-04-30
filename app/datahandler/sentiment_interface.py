from typing import List
import pandas as pd
from .db import Session, get_engine
from sqlmodel import select
from .models import ScraperResult
from loguru import logger

class SentimentDBInterface:
    def __init__(self, path_to_db=None) -> None:
        self.engine = get_engine(path_to_db)

    def insert_result_dataframe(self, df:pd.DataFrame):
        with Session(self.engine) as sess:
            for row_dict in df.to_dict(orient="records"):
                try:
                    res = ScraperResult(**row_dict)
                    sess.add(res)
                except:
                    logger.error(f'DB reuslt entry denied. Maybe dublicate. hash: {res.hash}')
            sess.commit()


    def get_last_hashes(self, platform:str, amount:int=50) -> List[str]:
        with Session(self.engine) as sess:
            statement = (
                select(ScraperResult.hash)
                .where(ScraperResult.origin == platform)
                .order_by(ScraperResult.published)
                .limit(amount)
                )
            res = sess.exec(statement).all()
            return res


    