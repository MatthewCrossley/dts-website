from uuid import uuid4
from fastapi import HTTPException
import pytest
from pytest_mock import MockerFixture
from db.models import User
from src.users import api
from mocks import MockSessionOrTable


def test_only_admin_can_delete_user(mocker: MockerFixture):
    session = MockSessionOrTable()
    mocker.patch.object(session, 'get', return_value=User(id=uuid4(), username='', password=''))
    non_admin = User(id=uuid4(), username='', password='')
    admin = User(id=uuid4(), username='', password='', admin=True)

    with pytest.raises(HTTPException):
        api.delete_user(uuid4(), session=session, user=non_admin)

    api.delete_user(uuid4(), session, admin)


def test_raises_404_if_user_not_found(mocker: MockerFixture):
    session = MockSessionOrTable()
    mocker.patch.object(session, 'get', return_value=None)
    user = User(id=uuid4(), username='', password='')

    with pytest.raises(HTTPException):
        api.read_user(uuid4(), session=session)

    with pytest.raises(HTTPException):
        api.update_user(uuid4(), user_details=User(id=uuid4()), session=session)

    with pytest.raises(HTTPException):
        api.delete_user(uuid4(), session=session, user=user)
