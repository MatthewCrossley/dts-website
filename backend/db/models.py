from sqlmodel import Field
from sqlmodel import SQLModel
from uuid import uuid4, UUID


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, unique=True)
    password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    password: str | None = None


class UserPublic(UserBase):
    id: UUID
