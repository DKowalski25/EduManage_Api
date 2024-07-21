from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from core import ErrorDetails

from .schemas import AssignedTask, AssignedTaskUpdate, AssignedTaskCreate
from .cases import AssignedTaskCases
from .container import Container

router = APIRouter(
    responses={
        401: {"model": ErrorDetails},
        404: {"model": ErrorDetails},
    }
)


@router.post('/assigned_tasks', response_model=AssignedTaskCreate)
@inject
async def create_assignment(
        assigned_task_create: AssignedTaskCreate,
        assigned_task_cases: AssignedTaskCases = Depends(Provide[Container.assigned_task_cases])
):
    return await assigned_task_cases.create_assigned_task(assigned_task_create)


@router.get('/assigned_tasks', response_model=list[AssignedTask])
@inject
async def get_all_assignments(
        assigned_task_cases: AssignedTaskCases = Depends(Provide[Container.assigned_task_cases])
):
    return await assigned_task_cases.get_all_assigned_tasks()


@router.get('/assigned_tasks/{assigned_task_id}', response_model=AssignedTask)
@inject
async def get_assignment_by_id(
        assigned_task_id: int,
        assigned_task_cases: AssignedTaskCases = Depends(Provide[Container.assigned_task_cases])
):
    return await assigned_task_cases.get_assigned_task_by_id(assigned_task_id)


@router.patch('/assigned_tasks/{assigned_task_id}', response_model=AssignedTask)
@inject
async def update_assignment(
        assigned_task_id: int,
        assigned_task_update: AssignedTaskUpdate,
        assigned_task_cases: AssignedTaskCases = Depends(Provide[Container.assigned_task_cases])
):
    return await assigned_task_cases.update_assignment(assigned_task_id, assigned_task_update)


@router.delete('/assigned_tasks/{assigned_task_id}', response_model=AssignedTask)
@inject
async def delete_assignment(
        assigned_task_id: int,
        assigned_task_cases: AssignedTaskCases = Depends(Provide[Container.assigned_task_cases])
):
    return await assigned_task_cases.delete_assigned_task(assigned_task_id)
