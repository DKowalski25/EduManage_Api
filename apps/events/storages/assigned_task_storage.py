from sqlalchemy.future import select

from datetime import datetime

from ..models import AssignedTask as AssignedTaskModel
from ..schemas import AssignedTask, AssignedTaskCreate, AssignmentUpdate

from db import async_session


class AssignedTaskStorage:
    _table = AssignedTaskModel

    @classmethod
    async def get_all_assigned_tasks(cls) -> list[AssignedTask]:
        async with async_session() as session:
            result = await session.execute(select(cls._table))
            return [AssignedTask.model_validate(task) for task in result.scalars().all()]

    @classmethod
    async def get_assigned_task_by_id(cls, assigned_task_id: int) -> AssignedTask:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == assigned_task_id))
            task = result.scalar()
            return AssignedTask.model_validate(task) if task else None

    @classmethod
    async def create_assigned_task(cls, assigned_task_create: AssignedTaskCreate) -> AssignedTask:
        async with async_session() as session:
            task = cls._table(**assigned_task_create.dict(), created_at=datetime.now())
            session.add(task)
            await session.commit()
            return AssignedTask.model_validate(task)

    @classmethod
    async def update_assigned_task(cls, assigned_task_id: int,
                                   assigned_task_update: AssignmentUpdate) -> AssignedTask | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == assigned_task_id))
            task = result.scalar()
            if task:
                for field, value in assigned_task_update.dict(exclude_unset=True).items():
                    setattr(task, field, value)
                await session.commit()
                return AssignedTask.model_validate(task)
            return None

    @classmethod
    async def delete_assigned_task(cls, assigned_task_id: int) -> AssignedTask | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == assigned_task_id))
            task = result.scalar()
            if task:
                session.delete(task)
                await session.commit()
                return AssignedTask.model_validate(task)
            return None
