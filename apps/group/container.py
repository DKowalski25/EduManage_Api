from dependency_injector import containers, providers

from .cases import GroupCases
from .storages import GroupStorage


class Container(containers.DeclarativeContainer):
    group_storage = providers.Singleton(
        GroupStorage
    )

    group_cases = providers.Singleton(
        GroupCases,
        group_repo=group_storage
    )
