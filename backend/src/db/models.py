from datetime import datetime
from uuid import UUID, uuid4

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(index=True, unique=True, min_length=5, max_length=128)


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, unique=True)
    password: str = Field(min_length=5, max_length=128)
    admin: bool = Field(default=False)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    admin: bool = False


class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=5, max_length=128)
    password: str | None = Field(default=None, min_length=5, max_length=128)


class UserPublic(UserBase):
    id: UUID
    admin: bool = False


class TaskBase(SQLModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(index=True, min_length=1, max_length=256)
    description: str | None = Field(default=None, max_length=2048)
    assigned_to: UUID | None = Field(foreign_key="user.id")
    due: datetime | None = None


class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, unique=True)
    created_by: UUID = Field(foreign_key="user.id")
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)


class TaskCreate(TaskBase):
    assigned_to: UUID | None = None


class TaskUpdate(TaskBase):
    title: str | None = Field(default=None, min_length=1, max_length=256)
    description: str | None = Field(default=None, max_length=2048)
    assigned_to: UUID | None = None
    completed: bool | None = None
    due: datetime | None = None


class TaskPublic(TaskBase):
    id: UUID
    created_by: UUID
    completed: bool
    created_at: datetime
