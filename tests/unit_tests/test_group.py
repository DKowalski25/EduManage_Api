import pytest
from dependency_injector.wiring import Provide, inject

from apps.group import schemas, storages
from apps.group.container import Container as GroupContainer


@pytest.fixture
def group_data():
    return schemas.GroupCreate(
        group_name="Math Group",
        description="Group for math students",
        grade=10,
    )


# @pytest.mark.with_db
@inject
async def test_group_creation(
        group_data: schemas.GroupCreate,
        group_storage: storages.GroupStorage = Provide[GroupContainer.group_storage],
):
    created_group = await group_storage.create_group(group_data)

    # Проверяем, что группа была создана и ей присвоен id
    assert created_group.id is not None

    # Проверяем, что данные группы были сохранены корректно
    assert created_group.group_name == group_data.group_name
    assert created_group.description == group_data.description
    assert created_group.grade == group_data.grade


# @pytest.mark.with_db
# @inject
# async def test_get_group_by_id(
#         group_data: schemas.GroupCreate,
#         group_storage: storages.GroupStorage = Provide['group_storage'],
# ):
#     created_group = await group_storage.create_group(group_data)
#     fetched_group = await group_storage.get_group_by_id(created_group.id)
#
#     # Проверяем, что группа была найдена и данные совпадают
#     assert fetched_group is not None
#     assert fetched_group.id == created_group.id
#     assert fetched_group.group_name == created_group.group_name
#     assert fetched_group.description == created_group.description
#     assert fetched_group.grade == created_group.grade
#
#
# @pytest.mark.with_db
# @inject
# async def test_update_group(
#         group_data: schemas.GroupCreate,
#         group_storage: storages.GroupStorage = Provide['group_storage'],
# ):
#     created_group = await group_storage.create_group(group_data)
#
#     update_data = schemas.GroupUpdate(
#         group_name="Updated Group Name",
#         description="Updated description",
#         grade=11
#     )
#
#     updated_group = await group_storage.update_group(created_group.id, update_data)
#
#     # Проверяем, что группа была обновлена и данные были изменены
#     assert updated_group.id == created_group.id
#     assert updated_group.group_name == update_data.group_name
#     assert updated_group.description == update_data.description
#     assert updated_group.grade == update_data.grade
#
#
# @pytest.mark.with_db
# @inject
# async def test_delete_group(
#         group_data: schemas.GroupCreate,
#         group_storage: storages.GroupStorage = Provide['group_storage'],
# ):
#     created_group = await group_storage.create_group(group_data)
#
#     deleted_group = await group_storage.delete_group(created_group.id)
#
#     # Проверяем, что группа была удалена
#     assert deleted_group is not None
#     assert deleted_group.id == created_group.id
#
#     # Проверяем, что группа не существует больше в базе данных
#     fetched_group = await group_storage.get_group_by_id(created_group.id)
#     assert fetched_group is None
