from ..storages.assigned_task_storage import AssignedTaskStorage
from ..storages.assignment_storage import AssignmentStorage
from ..schemas import AssignedTask, AssignedTaskCreate, AssignedTaskUpdate
from ..tasks.email_tasks import send_email_task

from apps.group.storages.group_storage import GroupStorage
from apps.users.storages.user_storage import UserStorage


class AssignedTaskCases:
    def __init__(self, assigned_task_repo: AssignedTaskStorage):
        self.assigned_task_repo = assigned_task_repo

    async def create_assigned_task(self, assigned_task_create: AssignedTaskCreate) \
            -> AssignedTask:
        assigned_task = await self.assigned_task_repo.create_assigned_task(assigned_task_create)

        assignment = await AssignmentStorage.get_assignment_by_id(assigned_task.assignment_id)

        if assigned_task.group_id:
            student_emails = await GroupStorage.get_emails_by_group_id(assigned_task.group_id)
        elif assigned_task.student_id:
            student_emails = [await UserStorage.get_email_by_student_id(assigned_task.student_id)]
        else:
            student_emails = []

        # Вызов задачи Celery для отправки email-уведомления каждому студенту
        for email in student_emails:
            send_email_task.delay(
                subject=f'{assignment.title} has been assigned to you',
                body=f'You have a new assignment: {assignment.description}\n'
                     f"Срок сдачи: {assignment.due_date.strftime('%Y-%m-%d')}",
                to_email=email
            )
            return assigned_task

        async def get_all_assigned_tasks(self) -> list[AssignedTask]:
            return await self.assigned_task_repo.get_all_assigned_tasks()

        async def get_assigned_task_by_id(self, assigned_task_id: int) -> AssignedTask:
            return await self.assigned_task_repo.get_assigned_task_by_id(assigned_task_id)

        async def update_assignment(self, assigned_task_id: int, assigned_task_update: AssignedTaskUpdate
                                    ) -> AssignedTask | None:
            return await self.assigned_task_repo.update_assigned_task(assigned_task_id, assigned_task_update)

        async def delete_assigned_task(self, assigned_task_id: int) -> AssignedTask | None:
            return await self.assigned_task_repo.delete_assigned_task(assigned_task_id)
