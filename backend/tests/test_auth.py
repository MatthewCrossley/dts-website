import pytest
from fastapi.exceptions import HTTPException
from mocks import MockCredentials, MockSessionOrTable
from src.auth import auth_check


@pytest.mark.asyncio
async def test_raises_error_if_unauthenticated():
    with pytest.raises(HTTPException):
        await auth_check(
            credentials=MockCredentials("username", "password"), session=MockSessionOrTable()
        )
