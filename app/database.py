from sqlmodel import create_engine
from typing import Annotated 
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .config import settings
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DB_URL_PYMYSQL = f"mysql+pymysql://{settings.database_username}{settings.database_password}:@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DB_URL_PYMYSQL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]