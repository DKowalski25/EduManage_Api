from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from core import ErrorDetails

from .schemas import Group, GroupCreate, GroupUpdate
from .cases import GroupCases
from .container import Container

router = APIRouter(
    responses={
        401: {"model": ErrorDetails},
        404: {"model": ErrorDetails},
    }
)


@router.post("/groups", response_model=Group)
@inject
async def create_group(
        group_create: GroupCreate,
        group_cases: GroupCases = Depends(Provide[Container.group_cases]),
):
    return await group_cases.create_group(group_create)


@router.get("/groups", response_model=list[Group])
@inject
async def get_all_groups(
        group_cases: GroupCases = Depends(Provide[Container.group_cases])
):
    return await group_cases.get_all_group()


@router.get("/groups/{group_id}", response_model=Group)
@inject
async def get_group_by_id(
        group_id: int,
        group_cases: GroupCases = Depends(Provide[Container.group_cases])
):
    return await group_cases.get_group_by_id(group_id)


@router.patch("/groups/{group_id}", response_model=Group)
@inject
async def update_group(
        group_id: int,
        group_update: GroupUpdate,
        group_cases: GroupCases = Depends(Provide[Container.group_cases]),
):
    return await group_cases.update_group(group_id, group_update)


@router.delete("/groups/{group_id}", response_model=Group)
@inject
async def delete_group(
        group_id: int,
        group_cases: GroupCases = Depends(Provide[Container.group_cases]),
):
    return await group_cases.delete_group(group_id)
