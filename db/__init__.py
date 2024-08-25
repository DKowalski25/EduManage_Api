from .orm import Base, async_session

__all__ = (
    'Base',
    'async_session',
)


def get_container():
    from db.containers import DatabaseContainer

    container = DatabaseContainer()
    container.wire(packages=[__name__])
    return container


container = get_container()
