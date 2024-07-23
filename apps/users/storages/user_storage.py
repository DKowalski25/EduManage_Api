import random
import hashlib
import string

from passlib.context import CryptContext
from sqlalchemy.future import select
from datetime import datetime

from sqlalchemy.orm import selectinload

from ..models import User as UserModel
from ..schemas import User, UserCreate, UserUpdate, FullUser

from db import async_session


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None) -> str:
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}${enc.hex()}"


def validate_password(password: str, hashed_password: str) -> bool:
    try:
        salt, hashed = hashed_password.split("$", 1)
    except ValueError:
        raise ValueError("Invalid hashed password format")
    return hash_password(password, salt) == hashed


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
            # Request to get all users with related data download
            stmt = select(cls._table).options(
                selectinload(cls._table.classes),
                selectinload(cls._table.assignments),
                selectinload(cls._table.assigned_tasks),
                selectinload(cls._table.marks)
            )
            result = await session.execute(stmt)
            users = result.scalars().all()

            return [User.model_validate(user) for user in users]

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> User | None:
        async with async_session() as session:
            query = await session.execute(select(cls._table).filter(cls._table.id == user_id))
            user = query.scalar()
        async with async_session() as session:
            # Reading a created user using selectonload
            stmt = select(cls._table).filter_by(id=user.id).options(
                selectinload(cls._table.classes),
                selectinload(cls._table.assignments),
                selectinload(cls._table.assigned_tasks),
                selectinload(cls._table.marks)
            )
            result = await session.execute(stmt)
            user = result.scalars().one_or_none()
        return User.model_validate(user) if user else None

    @classmethod
    async def get_user_by_identity(cls, email: str) -> FullUser | None:
        async with async_session() as session:
            query = await session.execute(select(cls._table).filter(cls._table.email == email))
            user = query.scalar()
        # Проверка, найден ли пользователь
        if user is None:
            return None

        async with async_session() as session:
            # Reading a created user using selectonload
            stmt = select(cls._table).filter_by(email=user.email).options(
                selectinload(cls._table.classes),
                selectinload(cls._table.assignments),
                selectinload(cls._table.assigned_tasks),
                selectinload(cls._table.marks)
            )
            result = await session.execute(stmt)
            user = result.scalars().one_or_none()
        return FullUser.model_validate(user) if user else None

    @classmethod
    async def create_user(cls, user_create: UserCreate) -> User:
        salt = get_random_string()
        hashed_password = hash_password(user_create.password, salt)
        async with async_session() as session:
            user = cls._table(
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                email=user_create.email,
                phone_number=user_create.phone_number,
                role=user_create.role,
                hashed_password=f"{salt}${hashed_password}",
            )
            session.add(user)
            await session.commit()
            # Executing a request to get a newly created user
        async with async_session() as session:
            # Reading a created user using selectonload
            stmt = select(cls._table).filter_by(id=user.id).options(
                selectinload(cls._table.classes),
                selectinload(cls._table.assignments),
                selectinload(cls._table.assigned_tasks),
                selectinload(cls._table.marks)
            )
            result = await session.execute(stmt)
            user = result.scalars().one_or_none()
        return User.model_validate(user)

    @classmethod
    async def update_user(cls, user_id: int, user_update: UserUpdate) -> User:
        async with async_session() as session:
            # Request for getting user with selectinload
            stmt = select(cls._table).filter(cls._table.id == user_id).options(
                selectinload(cls._table.classes),
                selectinload(cls._table.assignments),
                selectinload(cls._table.assigned_tasks),
                selectinload(cls._table.marks)
            )
            result = await session.execute(stmt)
            user = result.scalar_one()

            if user:
                # Updating user fields
                for field, value in user_update.dict(exclude_unset=True).items():
                    setattr(user, field, value)

                await session.commit()
            async with async_session() as session:
                # Reading a created user using selectonload
                stmt = select(cls._table).filter_by(id=user.id).options(
                    selectinload(cls._table.classes),
                    selectinload(cls._table.assignments),
                    selectinload(cls._table.assigned_tasks),
                    selectinload(cls._table.marks)
                )
                result = await session.execute(stmt)
                user = result.scalars().one_or_none()

            # Return updated user
            return User.model_validate(user)

    @classmethod
    async def delete_user(cls, user_id: int) -> User:
        async with async_session() as session:
            # Request for getting user with selectinload
            stmt = select(cls._table).filter(cls._table.id == user_id).options(
                selectinload(cls._table.classes),
                selectinload(cls._table.assignments),
                selectinload(cls._table.assigned_tasks),
                selectinload(cls._table.marks)
            )
            result = await session.execute(stmt)
            user = result.scalar()

            if user:
                # Delete user
                await session.delete(user)  # use await
                await session.commit()

            # Return deleted user
        return User.model_validate(user)
