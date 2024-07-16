from dependency_injector import containers, providers

from .cases import UserCases
from .storages import UserStorage


class Container(containers.DeclarativeContainer):
    user_storage = providers.Singleton(
        UserStorage,
    )

    user_cases = providers.Singleton(
        UserCases,
        user_repo=user_storage
    )
