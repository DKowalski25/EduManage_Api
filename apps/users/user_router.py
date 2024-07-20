from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Body

from core import ErrorDetails

from .schemas import UserBase, UserCreate, User
from .cases import UserCases
from .container import Container

router = APIRouter(
    responses={
        401: {"model": ErrorDetails},
        404: {"model": ErrorDetails},
    }
)


@router.post("/users", response_model=User)
@inject
async def create_user(
        user_create: UserCreate,
        user_cases: UserCases = Depends(Provide[Container.user_cases]),
):
    user = UserCreate(**user_create.dict(exclude_unset=True))
    return await user_cases.create_user(user)


# @router.get("/users", response_model=list[User])
# @inject
# async def get_all_users(
#         user_cases: UserCases = Depends(Provide[Container.user_cases])
# ):
#     return await user_cases.get_all_users()
#
#
# @router.get("/users/{user_id}", response_model=User)
# @inject
# async def get_user_by_id(
#         user_id: int,
#         user_cases: UserCases = Depends(Provide[Container.user_cases])
# ):
#     return await user_cases.get_user_by_id(user_id)
#
#
# @router.patch("/users/{user_id}", response_model=User)
# @inject
# async def update_user(
#         user_id: int,
#         user_update: UserUpdate,
#         user_cases: UserCases = Depends(Provide[Container.user_cases])
# ):
#     return await user_cases.update_user(user_id, user_update)
#
#
# @router.delete("/users/{user_id}", response_model=User)
# @inject
# async def delete_user(
#         user_id: int,
#         user_cases: UserCases = Depends(Provide[Container.user_cases])
# ):
#     return await user_cases.delete_user(user_id)
