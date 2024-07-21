from dependency_injector import containers, providers

from .cases import MarkCases, AssignmentCases, AssignedTaskCases
from .storages import MarkStorage, AssignmentStorage, AssignedTaskStorage


class Container(containers.DeclarativeContainer):
    mark_storage = providers.Singleton(
        MarkStorage
    )
    mark_cases = providers.Singleton(
        MarkCases,
        mark_repo=mark_storage
    )

    assignment_storage = providers.Singleton(
        AssignmentStorage
    )
    assignment_cases = providers.Singleton(
        AssignmentCases,
        assignment_repo=assignment_storage
    )

    # assigned_task_storage = providers.Singleton(
    #     AssignedTaskStorage
    # )
    # assigned_task_cases = providers.Singleton(
    #     AssignedTaskCases,
    #     assigned_task_repo=assigned_task_storage
    # )

