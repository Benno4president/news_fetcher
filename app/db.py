from sqlalchemy import create_engine
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
        # TODO this is illegal, fix - maybe remove to_sql and just use sqlachemy
        #with self.engine.begin() as conn:
            
            # TODO to_sql can throw value error.
            # TODO to_sql returns int or none, depending on rows affected, maybe?
        # TODO all of this is cursed
        #conn = self.engine.raw_connection()
        conn = self.engine.raw_connection()
        df.to_sql("sentiment_articles", con=conn, if_exists="fail", index=False, method="multi")


    def get_last_hashes(self, platform:str, amount:int=50) -> List[str]:
        query = f'''
            SELECT hash
            FROM sentiment_articles
            WHERE origin = {platform}
            ORDER BY time DESC
            LIMIT {amount};
        '''
        #with self.engine.begin() as conn:
        conn = self.engine.raw_connection()
        
        res = pd.read_sql(query, con=conn)
#            statement = (
#                select(ScraperResult.hash)
#                .where(ScraperResult.origin == platform)
#                .order_by(ScraperResult.published)
#                .limit(amount)
#                )
        return res


    




