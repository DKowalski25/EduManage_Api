# tests/unit_test/groups/conftest.py

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from apps.group.models import Group as GroupModel
from apps.group.schemas import GroupCreate, GroupUpdate
from apps.group.storages import GroupStorage
from apps.group.cases import GroupCases
from db import async_session


@pytest.fixture(scope="function")
async def group_data():
    """Возвращает данные для создания группы."""
    return GroupCreate(
        group_name="Test Group",
        description="This is a test group",
        grade=10
    )


@pytest.fixture(scope="function")
async def group_storage():
    """Возвращает экземпляр GroupStorage для работы с базой данных."""
    return GroupStorage()


@pytest.fixture(scope="function")
async def group_cases(group_storage):
    """Возвращает экземпляр GroupCases с внедренным GroupStorage."""
    return GroupCases(group_repo=group_storage)


@pytest.fixture(scope="function")
async def test_group(group_storage, group_data):
    """Создает и возвращает тестовую группу в базе данных."""
    return await group_storage.create_group(group_data)
