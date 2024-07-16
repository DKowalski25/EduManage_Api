from ..storages.assigned_task_storage import AssignedTaskStorage
from ..schemas import AssignedTask, AssignedTaskCreate, AssignedTaskUpdate


class AssignedTaskCases:
    def __init__(self, assigned_task_storage: AssignedTaskStorage):
        self.assigned_task_storage = assigned_task_storage

    async def create_assigned_task(self, assigned_task_create: AssignedTaskCreate) -> AssignedTask:
        return await self.assigned_task_storage.create_assigned_task(assigned_task_create)

    async def get_all_assigned_tasks(self) -> list[AssignedTask]:
        return await self.assigned_task_storage.get_all_assigned_tasks()

    async def get_assigned_task_by_id(self, assigned_task_id: int) -> AssignedTask:
        return await self.assigned_task_storage.get_assigned_task_by_id(assigned_task_id)

    async def delete_assigned_task(self, assigned_task_id: int) -> AssignedTask | None:
        return await self.assigned_task_storage.delete_assigned_task(assigned_task_id)
