from sqlalchemy.future import select

from datetime import datetime

from sqlalchemy.orm import selectinload

from ..models import AssignedTask as AssignedTaskModel
from ..schemas import AssignedTask, AssignedTaskCreate, AssignedTaskUpdate

from db import async_session


class AssignedTaskStorage:
    _table = AssignedTaskModel

    @classmethod
    async def get_all_assigned_tasks(cls) -> list[AssignedTask]:
        async with async_session() as session:
            stmt = select(cls._table).options(
                selectinload(cls._table.assignment),
                selectinload(cls._table.group),
                selectinload(cls._table.student)
            )
            result = await session.execute(stmt)
            tasks = result.scalars().all()
            return [AssignedTask.model_validate(task) for task in tasks]

    @classmethod
    async def get_assigned_task_by_id(cls, assigned_task_id: int) -> AssignedTask:
        async with async_session() as session:
            query = await session.execute(select(cls._table).filter(cls._table.id == assigned_task_id))
            task = query.scalar()
        async with async_session() as session:
            # Reading a created task using selectinload
            stmt = select(cls._table).filter_by(id=task.id).options(
                selectinload(cls._table.assignment),
                selectinload(cls._table.group),
                selectinload(cls._table.student)
            )
            result = await session.execute(stmt)
            task = result.scalars().one_or_none()
        return AssignedTask.model_validate(task)

    @classmethod
    async def create_assigned_task(cls, assigned_task_create: AssignedTaskCreate) -> AssignedTask:
        async with async_session() as session:
            # Создание нового объекта AssignedTask
            assigned_task = cls._table(
                assignment_id=assigned_task_create.assignment_id,
                group_id=assigned_task_create.group_id,
                student_id=assigned_task_create.student_id,
                assigned_at=datetime.now()  # или используйте task_create.assigned_at, если это предоставляется
            )
            session.add(assigned_task)
            await session.commit()

            # Получение созданного задания с подгрузкой связанных сущностей
            stmt = select(cls._table).filter_by(id=assigned_task.id).options(
                selectinload(cls._table.assignment),
                selectinload(cls._table.group),
                selectinload(cls._table.student)
            )
            result = await session.execute(stmt)
            assigned_task = result.scalar_one_or_none()
        return AssignedTask.model_validate(assigned_task)

    @classmethod
    async def update_assigned_task(cls, task_id: int, task_update: AssignedTaskUpdate) -> AssignedTask:
        async with async_session() as session:
            # Request for getting assigned task with selectinload
            stmt = select(cls._table).filter(cls._table.id == task_id).options(
                selectinload(cls._table.student),
                selectinload(cls._table.assignment),
                selectinload(cls._table.group)
            )
            result = await session.execute(stmt)
            assigned_task = result.scalar_one_or_none()

            if assigned_task:
                # Updating assigned task fields
                for field, value in task_update.dict(exclude_unset=True).items():
                    setattr(assigned_task, field, value)

                await session.commit()

            async with async_session() as session:
                # Reading the updated assigned task using selectinload
                stmt = select(cls._table).filter_by(id=task_id).options(
                    selectinload(cls._table.student),
                    selectinload(cls._table.assignment),
                    selectinload(cls._table.group)
                )
                result = await session.execute(stmt)
                assigned_task = result.scalars().one_or_none()

        return AssignedTask.model_validate(assigned_task)

    @classmethod
    async def delete_assigned_task(cls, assigned_task_id: int) -> AssignedTask | None:
        async with async_session() as session:
            # Request for getting mark with selectinload
            stmt = select(cls._table).filter_by(id=assigned_task_id).options(
                selectinload(cls._table.student),
                selectinload(cls._table.assignment),
                selectinload(cls._table.group)
            )
            result = await session.execute(stmt)
            assigned_task = result.scalar()

            if assigned_task:
                # Delete mark
                await session.delete(assigned_task)
                await session.commit()
        # Return deleted mark
        return AssignedTask.model_validate(assigned_task)

