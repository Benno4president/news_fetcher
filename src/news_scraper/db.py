from sqlalchemy import create_engine, exc
from loguru import logger
import pandas as pd
from configuration import Configuration 
from typing import List


def get_engine(echo=False):
    p = Configuration.db_path
    logger.info('Using DB at {}', p)
    engine = create_engine(p, echo=echo)
    return engine


class DatabaseInterface:
    def __init__(self) -> None:
        self.engine = get_engine()

    def insert_result_dataframe(self, df:pd.DataFrame):
        # TODO simplest but most error prone solution. if any extension is needed, a rewrite is due.
        conn = self.engine.raw_connection()
        df.to_sql("sentiment_articles", con=conn, if_exists="fail", index=False, method="multi")


    def get_last_hashes(self, platform:str, amount:int=50) -> List[str]:
        # TODO simplest but most error prone solution. if any extension is needed, a rewrite is due.
        query = f'''
            SELECT hash
            FROM sentiment_articles
            WHERE origin = {platform}
            ORDER BY time DESC
            LIMIT {amount};
        '''
        conn = self.engine.raw_connection()        
        res = pd.read_sql(query, con=conn)
        return res


class TestDatabaseInterface:
    def insert_result_dataframe(self, df):
        return

    def get_last_hashes(self, platform, amount):
        return []



