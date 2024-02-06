from typing import Annotated

from fastapi import Path, Depends
from fastapi.routing import APIRouter

from database import query, schemas
from utils.exceptions import UserNotFoundException
from utils.dependencies import DataBaseDep, oauth2_scheme

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
