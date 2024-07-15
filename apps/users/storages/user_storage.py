import random
import hashlib
import string

from passlib.context import CryptContext
from sqlalchemy.future import select

from datetime import datetime

from ..models import User as UserModel
from ..schemas import User, UserCreate, UserUpdate

from db import async_session


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserStorage:
    """
    This class is responsible for CRUD operations for User entity
    and responsible only for CRUD with minimal validations and mostly
    with queries to DB
    """
    _table = UserModel

    @classmethod
    async def get_all_users(cls) -> list[User]:
        async with async_session() as session:
            result = await session.execute(select(cls._table))
            return [User.model_validate(user) for user in result.scalars().all()]

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> User:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == user_id))
            user = result.scalar()
            return User.model_validate(user) if user else None

    @classmethod
    async def create_user(cls, user_create: UserCreate) -> User:
        salt = get_random_string()
        hashed_password = hash_password(user_create.password, salt)

        async with async_session() as session:
            user = cls._table(**user_create.dict(), hashed_password=f"{salt}${hashed_password}",
                              created_at=datetime.now())
            session.add(user)
            await session.commit()
            return User.model_validate(user)

    @classmethod
    async def update_user(cls, user_id: int, user_update: UserUpdate) -> User | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == user_id))
            user = result.scalar()
            if user:
                for field, value in user_update.dict(exclude_unset=True).items():
                    setattr(user, field, value)
                await session.commit()
                return User.model_validate(user)
            return None

    @classmethod
    async def delete_user(cls, user_id: int) -> User | None:
        async with async_session() as session:
            result = await session.execute(select(cls._table).filter(cls._table.id == user_id))
            user = result.scalar()
            if user:
                session.delete(user)
                await session.commit()
                return User.model_validate(user)
            return None
