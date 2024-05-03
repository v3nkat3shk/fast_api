from typing import Annotated

from fastapi import Path, Depends
from fastapi.routing import APIRouter

from database import query, schemas
from database.models import User
from utils.exceptions import UserNotFoundException
from utils.dependencies import DataBaseDep, oauth2_scheme, get_current_user

router = APIRouter(dependencies=[Depends(oauth2_scheme)])


@router.get("/users/", response_model=list[schemas.User], name="users")
def read_users(db: DataBaseDep, skip: int = 0, limit: int = 100):
    users = query.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: Annotated[int, Path(title="The Id of the user to get")],
    db: DataBaseDep
):
    db_user = query.get_user(db, user_id=user_id)
    if db_user is None:
        raise UserNotFoundException(user_id)
    return db_user


@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    db: DataBaseDep,
    user_id: Annotated[int, Path(title="The Id of the user to get")],
    payload: schemas.UserUpdate
):
    return query.update_user(db, user_id, payload)


@router.get("/current_user", response_model=schemas.User)
async def current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
