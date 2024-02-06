import datetime
from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette.datastructures import URL
from database import query, schemas

from routers import users, books

from database.models import Base
from database.database import engine
from database.schemas import Token, User
from utils.dependencies import (
    create_access_token, DataBaseDep,
    get_current_active_user,
    authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from utils.passwd import hashed_password

Base.metadata.create_all(bind=engine)

application = FastAPI(debug=True)


@application.get("/", include_in_schema=False)
def redirect_to_docs(request: Request) -> RedirectResponse:
    host_url = request.url.components.geturl() + "docs/"
    url = URL(host_url)
    return RedirectResponse(url)


@application.post(
    "/sign_up/",
    response_model=schemas.User,
    description="API for user sign up")
def sign_up_user(user: schemas.UserCreate, db: DataBaseDep):
    db_user = query.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    hashed_passwd = hashed_password(user.password)
    user.__setattr__("password", hashed_passwd)
    return query.create_user(db=db, user=user)


@application.post("/login")
async def login(
    db: DataBaseDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@application.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


origins = [
    "http://localhost",
    "http://localhost:8080",
]


application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

application.include_router(users.router)
application.include_router(books.router)
