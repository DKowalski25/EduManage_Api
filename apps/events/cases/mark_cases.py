from ..storages.mark_storage import MarkStorage
from ..schemas import Mark, MarkCreate, MarkUpdate


class MarkCases:
    def __init__(self, mark_repo: MarkStorage):
        self.mark_repo = mark_repo

    async def create_mark(self, mark_create: MarkCreate) -> Mark:
        return await self.mark_repo.create_mark(mark_create)

    async def get_all_marks(self) -> list[Mark]:
        return await self.mark_repo.get_all_marks()

    async def get_mark_by_id(self, mark_id: int) -> Mark:
        return await self.mark_repo.get_mark_by_id(mark_id)

    async def update_mark(self, mark_id: int, mark_update: MarkUpdate) -> Mark | None:
        return await self.mark_repo.update_mark(mark_id, mark_update)

    async def delete_mark(self, mark_id: int) -> Mark | None:
        return await self.mark_repo.delete_mark(mark_id)
