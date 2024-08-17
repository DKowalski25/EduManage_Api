import pytest


from apps.group.schemas import GroupCreate, GroupUpdate
from apps.group.cases import GroupCases
from .conftest import group_data, group_storage, group_cases, test_group


@pytest.mark.asyncio
class TestGroup:
    async def test_create_group(self, group_cases, group_data):
        """Тестирование создания группы."""
        group = await group_cases.create_group(group_data)
        assert group.group_name == group_data.group_name
        assert group.description == group_data.description
        assert group.grade == group_data.grade

    # async def test_get_all_groups(self, group_cases, test_group):
    #     """Тестирование получения всех групп."""
    #     groups = await group_cases.get_all_group()
    #     assert len(groups) > 0
    #     assert test_group.id in [group.id for group in groups]
    #
    # async def test_get_group_by_id(self, group_cases, test_group):
    #     """Тестирование получения группы по ID."""
    #     group = await group_cases.get_group_by_id(test_group.id)
    #     assert group is not None
    #     assert group.id == test_group.id
    #
    # async def test_update_group(self, group_cases, test_group):
    #     """Тестирование обновления группы."""
    #     group_update = GroupUpdate(
    #         group_name="Updated Group",
    #         description="This group has been updated",
    #         grade=11
    #     )
    #     updated_group = await group_cases.update_group(test_group.id, group_update)
    #     assert updated_group.group_name == group_update.group_name
    #     assert updated_group.description == group_update.description
    #     assert updated_group.grade == group_update.grade
    #
    # async def test_delete_group(self, group_cases, test_group):
    #     """Тестирование удаления группы."""
    #     deleted_group = await group_cases.delete_group(test_group.id)
    #     assert deleted_group is not None
    #
    #     group = await group_cases.get_group_by_id(test_group.id)
    #     assert group is None
