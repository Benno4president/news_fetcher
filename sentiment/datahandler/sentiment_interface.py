from typing import List
import pandas as pd
from .db import Session, engine
from sqlmodel import select
from .models import ScraperResult

class SentimentDBInterface:

    @staticmethod
    def insert_result_dataframe(df:pd.DataFrame):
        with Session(engine) as sess:
            for row_dict in df.to_dict(orient="records"):
                res = ScraperResult(**row_dict)
                sess.add(res)
            sess.commit()


    @staticmethod
    def get_last_hashes(platform:str, amount:int=50) -> List[str]:
        with Session(engine) as sess:
            statement = (
                select(ScraperResult.hash)
                .where(ScraperResult.origin == platform)
                .order_by(ScraperResult.published)
                .limit(amount)
                )
            res = sess.exec(statement).all()
            return res

