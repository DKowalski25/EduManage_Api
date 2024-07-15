from sqlalchemy.future import select

from datetime import datetime

from ..models import Mark as MarkModel
from ..schemas import Mark, MarkCreate, MarkUpdate

from db import async_session


class MarkStorage:
    _table = MarkModel

    @classmethod
    async def get_all_marks(cls) -> list[Mark]:
        async with async_session() as session:
            result = await session.execute(select(cls._table))
            return [Mark.model_validate(mark) for mark in result.scalars().all()]

    @classmethod
    async def get_mark_by_id(cls, mark_id: int) -> Mark:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == mark_id))
            mark = result.scalar()
            return Mark.model_validate(mark) if mark else None

    @classmethod
    async def create_mark(cls, mark_create: MarkCreate) -> Mark:
        async with async_session() as session:
            mark = cls._table(**mark_create.dict(), created_at=datetime.now())
            session.add(mark)
            await session.commit()
            return Mark.model_validate(mark)

    @classmethod
    async def update_mark(cls, mark_id: int, mark_update: MarkUpdate) -> Mark | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == mark_id))
            mark = result.scalar()
            if mark:
                for field, value in mark_update.dict(exclude_unset=True).items():
                    setattr(mark, field, value)
                await session.commit()
                return Mark.model_validate(mark)
            return None

    @classmethod
    async def delete_mark(cls, mark_id: int) -> Mark | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == mark_id))
            mark = result.scalar()
            if mark:
                session.delete(mark)
                await session.commit()
                return Mark.model_validate(mark)
            return None
