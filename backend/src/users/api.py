import logging

from auth import AuthCheckDep
from db import DBSessionDep
from db.models import User, UserCreate, UserPublic, UserUpdate
from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from sqlmodel import select

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user_details: UserCreate, session: DBSessionDep) -> UUID4:
    user = User(username=user_details.username, password=user_details.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User {user.username} created with ID {user.id}")
    return user.id


@router.get("/current")
def current_user(user: AuthCheckDep) -> UserPublic:
    return user


@router.get("/{user_id}")
def read_user(user_id: UUID4, session: DBSessionDep) -> UserPublic:
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User {user.username} retrieved with ID {user.id}")
    return user


@router.get("/")
def read_all_users(session: DBSessionDep) -> list[UserPublic]:
    users = session.exec(select(User)).all()
    logger.info(f"Retrieved {len(users)} users")
    return users


@router.delete("/{user_id}")
def delete_user(user_id: UUID4, session: DBSessionDep) -> None:
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    logger.info(f"User {user.username} deleted with ID {user.id}")


@router.patch("/{user_id}")
def update_user(
    user_id: UUID4, user_details: UserUpdate, session: DBSessionDep
) -> UserPublic:
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    if user_details.username:
        user.username = user_details.username
    if user_details.password:
        user.password = user_details.password
    session.commit()
    session.refresh(user)
    logger.info(f"User {user.username} updated with ID {user.id}")
    return user
