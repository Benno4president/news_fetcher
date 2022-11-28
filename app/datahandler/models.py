from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select


class ScraperResult(SQLModel, table=True):
    hash:str = Field(primary_key=True)
    origin:str
    title:str
    author:str
    published:str
    url:str
    text:str