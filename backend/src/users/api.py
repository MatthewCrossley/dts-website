import logging

from fastapi import APIRouter, HTTPException
from pydantic import UUID4

from db import DBSessionDep
from db.models import User, UserCreate, UserPublic, UserUpdate


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


@router.get("/{user_id}")
def read_user(user_id: UUID4, session: DBSessionDep) -> UserPublic:
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User {user.username} retrieved with ID {user.id}")
    return user


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
) -> User:
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
