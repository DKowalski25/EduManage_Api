from sqlalchemy.future import select

from sqlalchemy.orm import selectinload

from ..models import Group as GroupModel
from ..schemas import Group, GroupCreate, GroupUpdate

from db import async_session


class GroupStorage:
    _table = GroupModel

    # def __init__(self, session_maker=async_session):
    #     print(f"Using session_maker: {session_maker}")  # Debug line
    #     self.session_maker = session_maker

    @classmethod
    async def get_all_groups(cls) -> list[Group]:
        async with async_session() as session:
            # Request to get all users with related data download
            stmt = select(cls._table).options(
                selectinload(cls._table.teachers),
                selectinload(cls._table.students),
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            groups = result.scalars().all()
            return [Group.model_validate(group) for group in groups]

    @classmethod
    async def get_group_by_id(cls, group_id: int) -> Group | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == group_id))
            group = result.scalar()
        async with async_session() as session:
            # Request to get all users with related data download
            stmt = select(cls._table).filter_by(id=group.id).options(
                selectinload(cls._table.teachers),
                selectinload(cls._table.students),
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            group = result.scalars().one_or_none()
        return Group.model_validate(group) if group else None

    @classmethod
    async def create_group(cls, group_create: GroupCreate) -> Group:
        async with async_session() as session:
            group = cls._table(
                group_name=group_create.group_name,
                description=group_create.description,
                grade=group_create.grade,
            )
            session.add(group)
            await session.commit()
            # Executing a request to get a newly created user
        async with async_session() as session:
            # Reading a created user using selectonload
            stmt = select(cls._table).filter_by(id=group.id).options(
                selectinload(cls._table.teachers),
                selectinload(cls._table.students),
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            group = result.scalars().one_or_none()
        return Group.model_validate(group)

    @classmethod
    async def update_group(cls, group_id: int, group_update: GroupUpdate) -> Group | None:
        async with async_session() as session:
            # Request for getting user with selectinload
            stmt = select(cls._table).filter(cls._table.id == group_id).options(
                selectinload(cls._table.teachers),
                selectinload(cls._table.students),
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            group = result.scalar_one()

            if group:
                # Updating user fields
                for field, value in group_update.dict(exclude_unset=True).items():
                    setattr(group, field, value)

                await session.commit()
            async with async_session() as session:
                # Reading a created user using selectonload
                stmt = select(cls._table).filter_by(id=group.id).options(
                    selectinload(cls._table.teachers),
                    selectinload(cls._table.students),
                    selectinload(cls._table.assigned_tasks)
                )
                result = await session.execute(stmt)
                group = result.scalars().one_or_none()
            # Return updated user
            return Group.model_validate(group)

    @classmethod
    async def delete_group(cls, group_id: int) -> Group | None:
        async with async_session() as session:
            # Request for getting user with selectinload
            stmt = select(cls._table).filter(cls._table.id == group_id).options(
                selectinload(cls._table.teachers),
                selectinload(cls._table.students),
                selectinload(cls._table.assigned_tasks)
            )
            result = await session.execute(stmt)
            group = result.scalar()

            if group:
                # Delete user
                await session.delete(group)  # use await
                await session.commit()

            # Return deleted user
        return Group.model_validate(group)
