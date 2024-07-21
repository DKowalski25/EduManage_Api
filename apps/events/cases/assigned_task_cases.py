from ..storages.assigned_task_storage import AssignedTaskStorage
from ..schemas import AssignedTask, AssignedTaskCreate, AssignedTaskUpdate


class AssignedTaskCases:
    def __init__(self, assigned_task_repo: AssignedTaskStorage):
        self.assigned_task_repo = assigned_task_repo

    async def create_assigned_task(self, assigned_task_create: AssignedTaskCreate) -> AssignedTask:
        return await self.assigned_task_repo.create_assigned_task(assigned_task_create)

    async def get_all_assigned_tasks(self) -> list[AssignedTask]:
        return await self.assigned_task_repo.get_all_assigned_tasks()

    async def get_assigned_task_by_id(self, assigned_task_id: int) -> AssignedTask:
        return await self.assigned_task_repo.get_assigned_task_by_id(assigned_task_id)

    async def update_assignment(self, assigned_task_id: int, assigned_task_update: AssignedTaskUpdate
                                ) -> AssignedTask | None:
        return await self.assigned_task_repo.update_assigned_task(assigned_task_id, assigned_task_update)

    async def delete_assigned_task(self, assigned_task_id: int) -> AssignedTask | None:
        return await self.assigned_task_repo.delete_assigned_task(assigned_task_id)
