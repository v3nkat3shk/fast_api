from typing import Annotated

from fastapi import HTTPException, Path, status, Depends
from fastapi.routing import APIRouter

from server.database import query, schemas, models
from server.exceptions import UserNotFoundException
from server.dependencies import DataBaseDep, oauth2_scheme

router = APIRouter(dependencies=[Depends(oauth2_scheme)])


@router.post(
    "/sign_up/",
    response_model=schemas.User,
    description="API for user sign up")
def sign_up_user(user: schemas.UserCreate, db: DataBaseDep):
    db_user = query.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    return query.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.User)
def login(user: schemas.UserCreate, db: DataBaseDep):
    hash_password = query.hash_password(user.password)
    user = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.hashed_password == hash_password
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    return user


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
