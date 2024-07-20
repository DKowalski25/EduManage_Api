import random
import hashlib
import string
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.future import select
from datetime import datetime

# from apps.group.models.group import Group as GroupModel
from ..models import User as UserModel
from ..schemas import UserBase, UserCreate, User

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
    async def create_user(cls, user_create: UserCreate) -> User:
        salt, hashed_password = hash_password(user_create.password)
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
            return User.from_orm(user)


