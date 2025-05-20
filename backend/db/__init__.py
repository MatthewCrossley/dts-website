from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlmodel import Session


engine = create_engine("sqlite:///database.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(get_session)]

def startup():
    create_db_and_tables()
