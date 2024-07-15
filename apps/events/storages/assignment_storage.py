from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from ..models.assignment import Assignment as AssignmentModel
from ..schemas.assignment import Assignment, AssignmentCreate, AssignmentUpdate
from db import async_session


class AssignmentStorage:
    _table = AssignmentModel

    @classmethod
    async def get_all_assignments(cls) -> list[Assignment]:
        async with async_session() as session:
            result = await session.execute(select(cls._table))
            return [Assignment.model_validate(assignment) for assignment in result.scalars().all()]

    @classmethod
    async def get_assignment_by_id(cls, assignment_id: int) -> Assignment:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == assignment_id))
            assignment = result.scalar()
            return Assignment.model_validate(assignment) if assignment else None

    @classmethod
    async def create_assignment(cls, assignment_create: AssignmentCreate) -> Assignment:
        async with async_session() as session:
            assignment = cls._table(**assignment_create.dict(), created_at=datetime.now())
            session.add(assignment)
            await session.commit()
            return Assignment.model_validate(assignment)

    @classmethod
    async def update_assignment(cls, assignment_id: int, assignment_update: AssignmentUpdate) -> Assignment | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == assignment_id))
            assignment = result.scalar()
            if assignment:
                for field, value in assignment_update.dict(exclude_unset=True).items():
                    setattr(assignment, field, value)
                await session.commit()
                return Assignment.model_validate(assignment)
            return None

    @classmethod
    async def delete_assignment(cls, assignment_id: int) -> Assignment | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == assignment_id))
            assignment = result.scalar()
            if assignment:
                session.delete(assignment)
                await session.commit()
                return Assignment.model_validate(assignment)
            return None
