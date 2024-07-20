import random
import hashlib
import string
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.future import select
from datetime import datetime

from apps.group.models.group import Group as GroupModel
from ..models import User as UserModel
from ..schemas import User, UserCreate, UserUpdate

from db import async_session


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return salt, f"${enc.hex()}"


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt)[1] == hashed


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserStorage:
    """
    This class is responsible for CRUD operations for User entity
    and responsible only for CRUD with minimal validations and mostly
    with queries to DB.
    """
    _table = UserModel

    @classmethod
    async def get_all_users(cls) -> list[User]:
        async with async_session() as session:
            result = await session.execute(select(cls._table))
            users = result.scalars().all()
            for user in users:
                await user.awaitable_attrs.group
                await user.awaitable_attrs.assignments
                await user.awaitable_attrs.assigned_tasks
                await user.awaitable_attrs.marks
        return [User.model_validate(user) for user in users]

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional[User]:
        async with async_session() as session:
            query = await session.execute(select(cls._table).filter(cls._table.id == user_id))
            user = query.scalar()
            if user:
                await user.awaitable_attrs.group
                await user.awaitable_attrs.assignments
                await user.awaitable_attrs.assigned_tasks
                await user.awaitable_attrs.marks
        return User.model_validate(user) if user else None

    @classmethod
    async def create_user(cls, user_create: UserCreate) -> Optional[User]:
        salt, hashed_password = hash_password(user_create.password)
        async with async_session() as session:
            async with session.begin():
                user = cls._table(
                    first_name=user_create.first_name,
                    last_name=user_create.last_name,
                    email=user_create.email,
                    phone_number=user_create.phone_number,
                    role=user_create.role,
                    hashed_password=f"{salt}${hashed_password}",
                    created_at=datetime.now()
                )
                if user_create.group_id:
                    group = await session.get(GroupModel, user_create.group_id)
                    if group:
                        user.group = group

                session.add(user)
                await session.commit()
                # await session.refresh(user)
                # Инициализируем атрибуты внутри транзакции
                print(user)
                await user.awaitable_attrs.group
                await user.awaitable_attrs.assignments
                await user.awaitable_attrs.assigned_tasks
                await user.awaitable_attrs.marks
                return User.model_validate(user)

    @classmethod
    async def update_user(cls, user_id: int, user_update: UserUpdate) -> Optional[User]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(cls._table).filter(cls._table.id == user_id))
                user = result.scalar()
                if user:
                    for field, value in user_update.dict(exclude_unset=True).items():
                        setattr(user, field, value)
                    await session.commit()
                    await session.refresh(user)
                    # Инициализируем атрибуты внутри транзакции
                    await user.awaitable_attrs.group
                    await user.awaitable_attrs.assignments
                    await user.awaitable_attrs.assigned_tasks
                    await user.awaitable_attrs.marks
                    return User.model_validate(user)
        return None

    @classmethod
    async def delete_user(cls, user_id: int) -> Optional[User]:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(cls._table).filter(cls._table.id == user_id))
                user = result.scalar()
                if user:
                    session.delete(user)
                    await session.commit()
                    # Инициализируем атрибуты внутри транзакции
                    await user.awaitable_attrs.group
                    await user.awaitable_attrs.assignments
                    await user.awaitable_attrs.assigned_tasks
                    await user.awaitable_attrs.marks
                    return User.model_validate(user)
        return None