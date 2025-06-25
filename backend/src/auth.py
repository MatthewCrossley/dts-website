import logging
from typing import Annotated

from .db import DBSessionDep
from .db.models import User
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import select

logger = logging.getLogger(__name__)
security = HTTPBasic()


async def auth_check(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session: DBSessionDep,
) -> User:
    user = session.exec(
        select(User).where(
            User.username == credentials.username
            and User.password == credentials.password
        )
    ).one_or_none()
    if not user:
        logger.warning(f"Authentication failed for user {credentials.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logger.info(f"User {credentials.username} authenticated successfully")
    return user


AuthCheckDep = Annotated[User, Depends(auth_check)]
