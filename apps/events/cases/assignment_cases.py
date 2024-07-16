from ..storages.assignment_storage import AssignmentStorage
from ..schemas import Assignment, AssignmentCreate, AssignmentUpdate


class AssignmentCases:
    def __init__(self, assignment_repo: AssignmentStorage):
        self.assignment_repo = assignment_repo

    async def create_assignment(self, assignment_create: AssignmentCreate) -> Assignment:
        return await self.assignment_repo.create_assignment(assignment_create)

    async def get_all_assignments(self) -> list[Assignment]:
        return await self.assignment_repo.get_all_assignments()

    async def get_assignment_by_id(self, assignment_id: int) -> Assignment:
        return await self.assignment_repo.get_assignment_by_id(assignment_id)

    async def update_assignment(self, assignment_id: int, assignment_update: AssignmentUpdate) -> Assignment | None:
        return await self.assignment_repo.update_assignment(assignment_id, assignment_update)

    async def delete_assignment(self, assignment_id: int) -> Assignment | None:
        return await self.assignment_repo.delete_assignment(assignment_id)
