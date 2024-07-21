from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from core import ErrorDetails

from .schemas import Mark, MarkCreate, MarkUpdate
from .cases import MarkCases
from .container import Container


router = APIRouter(
    responses={
        401: {"model": ErrorDetails},
        404: {"model": ErrorDetails},
    }
)


@router.post('/marks', response_model=Mark)
@inject
async def create_mark(
        mark_create: MarkCreate,
        mark_cases: MarkCases = Depends(Provide[Container.mark_cases])
):
    return await mark_cases.create_mark(mark_create)


@router.get('/marks', response_model=list[Mark])
@inject
async def get_all_marks(
        mark_cases: MarkCases = Depends(Provide[Container.mark_cases])
):
    return await mark_cases.get_all_marks()


@router.get('/marks/{mark_id}', response_model=Mark)
@inject
async def get_mark_by_id(
        mark_id: int,
        mark_cases: MarkCases = Depends(Provide[Container.mark_cases])
):
    return await mark_cases.get_mark_by_id(mark_id)


@router.patch('/marks/{mark_id}', response_model=Mark)
@inject
async def update_mark(
        mark_id: int,
        mark_update: MarkUpdate,
        mark_cases: MarkCases = Depends(Provide[Container.mark_cases])
):
    return await mark_cases.update_mark(mark_id, mark_update)


@router.delete('/marks/{mark_id}', response_model=Mark)
@inject
async def delete_mark(
        mark_id: int,
        mark_cases: MarkCases = Depends(Provide[Container.mark_cases])
):
    return await mark_cases.delete_mark(mark_id)