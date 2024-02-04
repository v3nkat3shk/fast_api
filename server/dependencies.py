from typing import Annotated, Generator, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.database import get_db
from database.schemas import User
from database import query


DataBaseDep = Annotated[Generator[Session, Any, None], Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def fake_hash_password(password: str):
    return password


class UserInDB(User):
    hashed_password: str


def get_user(username: str, db: DataBaseDep):
    user = query.get_user_by_email(db, username)
    if user:
        return user


def fake_decode_token(db: DataBaseDep, token):
    user = get_user(token, db)
    return user


async def get_current_user(
    db: DataBaseDep,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    user = fake_decode_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
