from sqlalchemy.future import select

from datetime import datetime

from sqlalchemy.orm import selectinload

from ..models import Mark as MarkModel
from ..schemas import Mark, MarkCreate, MarkUpdate

from db import async_session


class MarkStorage:
    _table = MarkModel

    @classmethod
    async def get_all_marks(cls) -> list[Mark]:
        async with async_session() as session:
            # Request to get all marks with related data download
            stmt = select(cls._table).options(
                selectinload(cls._table.student),
                selectinload(cls._table.assignment)
            )
            result = await session.execute(stmt)
            marks = result.scalars().all()

            return [Mark.model_validate(mark) for mark in marks]

    @classmethod
    async def get_mark_by_id(cls, mark_id: int) -> Mark | None:
        async with async_session() as session:
            query = await session.execute(select(cls._table).filter(cls._table.id == mark_id))
            mark = query.scalar()
        async with async_session() as session:
            # Reading a created mark using selectonload
            smtm = select(cls._table).filter_by(id=mark.id).options(
                selectinload(cls._table.student),
                selectinload(cls._table.assignment)
            )
            result = await session.execute(smtm)
            mark = result.scalars().one_or_none()
        return Mark.model_validate(mark) if mark else None

    @classmethod
    async def create_mark(cls, mark_create: MarkCreate) -> Mark:
        async with async_session() as session:
            mark = cls._table(
                value=mark_create.value,
                student_id=mark_create.student_id,
                assignment_id=mark_create.assignment_id,
                date=datetime.now()
            )
            session.add(mark)
            await session.commit()
            # Executing a request to get a newly created mark
            stmt = select(cls._table).filter_by(id=mark.id).options(
                selectinload(cls._table.student),
                selectinload(cls._table.assignment)
            )
            result = await session.execute(stmt)
            mark = result.scalars().one_or_none()
        return Mark.model_validate(mark)

    @classmethod
    async def update_mark(cls, mark_id: int, mark_update: MarkUpdate) -> Mark | None:
        async with async_session() as session:
            # Request for getting mark with selectinload
            stmt = select(cls._table).filter(cls._table.id == mark_id).options(
                selectinload(cls._table.student),
                selectinload(cls._table.assignment)
            )
            result = await session.execute(stmt)
            mark = result.scalar_one()

            if mark:
                # Updating mark fields
                for field, value in mark_update.dict(exclude_unset=True).items():
                    setattr(mark, field, value)

                await session.commit()
            async with async_session() as session:
                # Reading a created mark using selectonload
                stmt = select(cls._table).filter_by(id=mark.id).options(
                    selectinload(cls._table.student),
                    selectinload(cls._table.assignment)
                )
                result = await session.execute(stmt)
                mark = result.scalars().one_or_none()
            # Return updated mark
            return Mark.model_validate(mark)

    @classmethod
    async def delete_mark(cls, mark_id: int) -> Mark | None:
        async with async_session() as session:
            # Request for getting mark with selectinload
            stmt = select(cls._table).filter(cls._table.id == mark_id).options(
                selectinload(cls._table.student),
                selectinload(cls._table.assignment)
            )
            result = await session.execute(stmt)
            mark = result.scalar()

            if mark:
                # Delete mark
                session.delete(mark)
                await session.commit()
        # Return deleted mark
        return Mark.model_validate(mark)
