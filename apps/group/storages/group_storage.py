from sqlalchemy.future import select

from datetime import datetime

from ..models import Group as GroupModel
from ..schemas import Group, GroupCreate, GroupUpdate

from db import async_session


class GroupStorage:
    _table = GroupModel

    @classmethod
    async def get_all_groups(cls) -> list[Group]:
        async with async_session() as session:
            result = await session.execute(select(cls._table))
            return [Group.model_validate(group) for group in result.scalars().all()]

    @classmethod
    async def get_group_by_id(cls, group_id: int) -> Group:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == group_id))
            group = result.scalar()
            return Group.model_validate(group) if group else None

    @classmethod
    async def create_group(cls, group_create: GroupCreate) -> Group:
        async with async_session() as session:
            group = cls._table(**group_create.dict(), created_at=datetime.now())
            session.add(group)
            await session.commit()
            return Group.model_validate(group)

    @classmethod
    async def update_group(cls, user_id: int, group_update: GroupUpdate) -> Group | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == user_id))
            group = result.scalar()
            if group:
                for field, value in group_update.dict(exclude_unset=True).items():
                    setattr(group, field, value)
                await session.commit()
                return Group.model_validate(group)
            return None

    @classmethod
    async def delete_group(cls, group_id: int) -> Group | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == group_id))
            group = result.scalar()
            if group:
                session.delete(group)
                await session.commit()
                return Group.model_validate(group)
            return None
