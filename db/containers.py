from dependency_injector import containers, providers

from db.orm import async_session

from apps.group.container import Container as GroupContainer
from apps.events.container import Container as EventsContainer
from apps.users.features.auth.containers import Container as UserContainer


class DatabaseContainer(containers.DeclarativeContainer):
    """Контейнер для базы данных"""

    # Поставщик для базы данных
    session = providers.Singleton(async_session)

    group_storage = providers.Singleton(GroupContainer.group_storage)
    mark_storage = providers.Singleton(EventsContainer.mark_storage)
    assignment_storage = providers.Singleton(EventsContainer.assignment_storage)
    user_storage = providers.Singleton(UserContainer.user_storage)


# Экспортируем экземпляр контейнера для использования в тестах
db_container = DatabaseContainer()
