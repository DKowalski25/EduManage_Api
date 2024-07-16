from ..storages import GroupStorage
from ..schemas import Group, GroupCreate, GroupUpdate


class GroupCases:
    def __init__(self, group_repo: GroupStorage) -> None:
        self.group_repo = group_repo

    async def create_group(self, group_create: GroupCreate) -> Group:
        return await self.group_repo.create_group(group_create)

    async def get_all_group(self) -> list[Group]:
        return await self.group_repo.get_all_groups()

    async def get_group_by_id(self, group_id: int) -> Group:
        return await self.group_repo.get_group_by_id(group_id)

    async def update_group(self, group_id: int, group_update: GroupUpdate) -> Group | None:
        return await self.group_repo.update_group(group_id, group_update)

    async def delete_group(self, group_id: int) -> Group | None:
        return await self.group_repo.delete_group(group_id)
