from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from core import ErrorDetails, BaseRoute, IsAuthenticated

from .schemas import Assignment, AssignmentCreate, AssignmentUpdate
from .cases import AssignmentCases
from .container import Container

router = APIRouter(
    route_class=BaseRoute,
    dependencies=[Depends(IsAuthenticated())],
    responses={
        401: {"model": ErrorDetails},
        404: {"model": ErrorDetails},
    }
)


@router.post('/assignments', response_model=Assignment)
@inject
async def create_assignment(
        assignment_create: AssignmentCreate,
        assignment_cases: AssignmentCases = Depends(Provide[Container.assignment_cases])
):
    return await assignment_cases.create_assignment(assignment_create)


@router.get('/assignments', response_model=list[Assignment])
@inject
async def get_all_assignments(
        assignment_cases: AssignmentCases = Depends(Provide[Container.assignment_cases])
):
    return await assignment_cases.get_all_assignments()


@router.get('/assignments/{assignment_id}', response_model=Assignment)
@inject
async def get_assignment_by_id(
        assignment_id: int,
        assignment_cases: AssignmentCases = Depends(Provide[Container.assignment_cases])
):
    return await assignment_cases.get_assignment_by_id(assignment_id)


@router.patch('/assignments/{assignment_id}', response_model=Assignment)
@inject
async def update_assignment(
        assignment_id: int,
        assignment_update: AssignmentUpdate,
        assignment_cases: AssignmentCases = Depends(Provide[Container.assignment_cases])
):
    return await assignment_cases.update_assignment(assignment_id, assignment_update)


@router.delete('/assignments/{assignment_id}', response_model=Assignment)
@inject
async def delete_assignment(
        assignment_id: int,
        assignment_cases: AssignmentCases = Depends(Provide[Container.assignment_cases])
):
    return await assignment_cases.delete_assignment(assignment_id)
