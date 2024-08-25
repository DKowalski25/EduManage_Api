from dependency_injector import containers, providers

from apps.group.storages import GroupStorage
from db.orm import async_session

from apps.group.container import Container as GroupContainer


class DatabaseContainer(containers.DeclarativeContainer):
    """Контейнер для базы данных"""

    # Поставщик для базы данных
    session = providers.Singleton(async_session)

    group_storage = providers.Singleton(GroupContainer.group_storage)


# Экспортируем экземпляр контейнера для использования в тестах
db_container = DatabaseContainer()
