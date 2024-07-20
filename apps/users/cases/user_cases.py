from ..storages import UserStorage
from ..schemas import UserBase, UserCreate, User


class UserCases:
    def __init__(self, user_repo: UserStorage) -> None:
        self._user_repo = user_repo

    async def create_user(self, user_create: UserCreate) -> User:
        return await self._user_repo.create_user(user_create)

    # async def get_all_users(self) -> list[User]:
    #     return await self.user_repo.get_all_users()
    #
    # async def get_user_by_id(self, user_id: int) -> User:
    #     return await self.user_repo.get_user_by_id(user_id)
    #
    # async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
    #     return await self.user_repo.update_user(user_id, user_update)
    #
    # async def delete_user(self, user_id: int) -> User:
    #     return await self.user_repo.delete_user(user_id)
