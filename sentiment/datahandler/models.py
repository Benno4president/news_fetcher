from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

"""
class Strategy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    score: int = 0
    hyperopt_id: Optional[int] = Field(default=None, foreign_key=True)
"""

class ScraperResult(SQLModel, table=True):
    hash:str = Field(primary_key=True)
    origin:str
    title:str
    author:str
    published:str
    sentiment:str
    url:str
    text:str