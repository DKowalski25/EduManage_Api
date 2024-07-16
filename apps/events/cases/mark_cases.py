from ..storages.mark_storage import MarkStorage
from ..schemas import Mark, MarkCreate, MarkUpdate


class MarkCases:
    def __init__(self, mark_storage: MarkStorage):
        self.mark_storage = mark_storage

    async def create_mark(self, mark_create: MarkCreate) -> Mark:
        return await self.mark_storage.create_mark(mark_create)

    async def get_all_marks(self) -> list[Mark]:
        return await self.mark_storage.get_all_marks()

    async def get_mark_by_id(self, mark_id: int) -> Mark:
        return await self.mark_storage.get_mark_by_id(mark_id)

    async def update_mark(self, mark_id: int, mark_update: MarkUpdate) -> Mark | None:
        return await self.mark_storage.update_mark(mark_id, mark_update)

    async def delete_mark(self, mark_id: int) -> Mark | None:
        return await self.mark_storage.delete_mark(mark_id)
