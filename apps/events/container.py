from dependency_injector import containers, providers

from .cases import MarkCases
from .storages import MarkStorage


class Container(containers.DeclarativeContainer):
    mark_storage = providers.Singleton(
        MarkStorage
    )
    mark_cases = providers.Singleton(
        MarkCases,
        mark_repo=mark_storage
    )
