import time
from datetime import datetime
from random import choice, randint
from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, select

from .models import Task, User

engine = create_engine("sqlite:///database.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def seed_data():
    with Session(engine) as session:
        users = list(session.exec(select(User)).all())
        while len(users) < 10:
            random_number = randint(1, 1_000_000)
            user = User(
                username=f"user{random_number}",
                id=uuid4(),
                password=f"password{random_number}",
                admin=random_number % 2 == 0,  # Randomly assign admin status
            )
            session.add(user)
            users.append(user)

        tasks = list(session.exec(select(Task)).all())
        while len(tasks) < 10:
            random_number = randint(1, 1_000_000)
            task = Task(
                title=f"Some task {random_number}",
                id=uuid4(),
                description=f"This task was created with random number {random_number}",
                assigned_to=choice(users).id,
                created_by=choice(users).id,
                completed=random_number % 2 == 0,
                due=datetime.fromtimestamp(time.time() + random_number),
            )
            session.add(task)
            tasks.append(task)

        session.commit()


def get_session():
    with Session(engine) as session:
        yield session


def startup():
    create_db_and_tables()
    seed_data()


DBSessionDep = Annotated[Session, Depends(get_session)]
