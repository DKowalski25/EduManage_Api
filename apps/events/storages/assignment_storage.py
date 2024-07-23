from sqlalchemy.future import select

from datetime import datetime

from sqlalchemy.orm import selectinload

from ..models.assignment import Assignment as AssignmentModel
from ..schemas.assignment import Assignment, AssignmentCreate, AssignmentUpdate, AssignmentBase

from apps.users.models.user import User as UserModel
from db import async_session


class AssignmentStorage:
    _table = AssignmentModel

    @classmethod
    async def get_all_assignments(cls) -> list[Assignment]:
        async with async_session() as session:
            stmt = select(cls._table).options(
                selectinload(cls._table.teacher),
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            assignments = result.scalars().all()
            # Преобразование в схемы Pydantic
            return [
                Assignment(
                    id=assignment.id,
                    title=assignment.title,
                    description=assignment.description,
                    due_date=assignment.due_date,
                    created_at=assignment.created_at,
                    teacher_id=assignment.teacher_id,
                    assigned_tasks=[task.id for task in assignment.assigned_tasks]
                ) for assignment in assignments
            ]
            # return [Assignment.from_orm(assignment) for assignment in assignments]

    @classmethod
    async def get_assignment_by_id(cls, assignment_id: int) -> Assignment:
        async with async_session() as session:
            query = await session.execute(select(cls._table).filter(cls._table.id == assignment_id))
            assignment = query.scalar()
        async with async_session() as session:
            # Reading a created assignment using selectinload
            stmt = select(cls._table).filter_by(id=assignment.id).options(
                selectinload(cls._table.teacher),
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            assignment = result.scalars().one_or_none()

        return Assignment.model_validate(assignment)

    @classmethod
    async def create_assignment(cls, assignment_create: AssignmentCreate) -> Assignment:
        async with async_session() as session:
            # Checking if teacher_id exists
            teacher_stmt = select(UserModel).filter_by(id=assignment_create.teacher_id)
            teacher_result = await session.execute(teacher_stmt)
            teacher_exists = teacher_result.scalar_one_or_none()

            if not teacher_exists:
                raise ValueError(f"Teacher with id {assignment_create.teacher_id} does not exist.")

            assignment = cls._table(
                title=assignment_create.title,
                description=assignment_create.description,
                due_date=assignment_create.due_date,
                created_at=datetime.now(),
                teacher_id=assignment_create.teacher_id
            )
            session.add(assignment)
            await session.commit()
            # await session.refresh(assignment)  # updating the object to get the id

            # Executing a request to get a newly created record using selectinload
            stmt = select(cls._table).filter_by(id=assignment.id).options(
                selectinload(cls._table.teacher),
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            assignment = result.scalars().one_or_none()

        return Assignment.model_validate(assignment)

    @classmethod
    async def update_assignment(cls, assignment_id: int, assignment_update: AssignmentUpdate) -> Assignment | None:
        async with async_session() as session:
            # Checking if the task exists
            assignment_stmt = select(cls._table).filter_by(id=assignment_id)
            assignment_result = await session.execute(assignment_stmt)
            assignment = assignment_result.scalar_one_or_none()

            if not assignment:
                raise ValueError(f"Assignment with id {assignment_id} does not exist.")

            # Updating the task fields
            for field, value in assignment_update.dict(exclude_unset=True).items():
                setattr(assignment, field, value)

            # If the teacher_id is updated, we check its existence
            if 'teacher_id' in assignment_update.dict(exclude_unset=True):
                teacher_stmt = select(UserModel).filter_by(id=assignment_update.teacher_id)
                teacher_result = await session.execute(teacher_stmt)
                teacher_exists = teacher_result.scalar_one_or_none()

                if not teacher_exists:
                    raise ValueError(f"Teacher with id {assignment_update.teacher_id} does not exist.")

                assignment.teacher_id = assignment_update.teacher_id

            await session.commit()
            await session.refresh(assignment)  # Updating the object to get up-to-date data

            # Executing a request to get an updated record using select in load
            stmt = select(cls._table).filter_by(id=assignment.id).options(
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            assignment = result.scalars().one_or_none()

        return Assignment.model_validate(assignment) if assignment else None

    @classmethod
    async def delete_assignment(cls, assignment_id: int) -> Assignment | None:
        async with async_session() as session:
            # Checking if the task exists
            assignment_stmt = select(cls._table).filter_by(id=assignment_id)
            assignment_result = await session.execute(assignment_stmt)
            assignment = assignment_result.scalar_one_or_none()

            if not assignment:
                raise ValueError(f"Assignment with id {assignment_id} does not exist.")

            # Delete task
            await session.delete(assignment)
            await session.commit()

            # # Executing a request to get a deleted record using select in load
            # stmt = select(cls._table).filter_by(id=assignment.id).options(
            #     selectinload(cls._table.assigned_tasks)
            # )
            # result = await session.execute(stmt)
            # assignment = result.scalars().one_or_none()

        return Assignment.model_validate(assignment)
