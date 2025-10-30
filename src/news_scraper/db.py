from typing import List
from loguru import logger
import pandas as pd
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from configuration import Configuration 

def get_engine(echo=False):
    p = Configuration.db_path
    logger.info('Using DB at {}', p)
    engine = create_engine(p, echo=echo)
    return engine


class DatabaseInterface:
    def __init__(self) -> None:
        self.engine = get_engine()
        self._metadata = MetaData()
        self.articles_table = Table("articles", self._metadata, autoload_with=self.engine)

    def insert_result_dataframe(self, df:pd.DataFrame):
        if df.empty:
            return

        table_cols = [c.name for c in self.articles_table.columns]
        df = df.loc[:, df.columns.intersection(table_cols)]
        df = df[[c for c in table_cols if c in df.columns]]
        records = df.to_dict(orient="records")
        if not records:
            return

        with Session(self.engine) as session:
            try:
                session.execute(self.articles_table.insert(), records)
                session.commit()
            except Exception:
                session.rollback()
                raise


    def get_last_hashes(self, platform:str, amount:int=50) -> List[str]:
        sql = text("""
            SELECT hash
            FROM articles
            WHERE origin = :platform
            ORDER BY published DESC
            LIMIT :limit
        """)
        params = {"platform": platform, "limit": int(amount)}

        with self.engine.connect() as conn:
            result = conn.execute(sql, params)
            rows = [row["hash"] for row in result.fetchall()]
        return rows

class TestDatabaseInterface:
    def insert_result_dataframe(self, df):
        return

    def get_last_hashes(self, platform, amount):
        return []



