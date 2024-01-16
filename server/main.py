from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette.datastructures import URL

from server.routers import users, books

from server.database.models import Base
from server.database.database import engine
from server.dependencies import DataBaseDep
from server.database.schemas import User
from server.dependencies import (
    get_user, fake_hash_password, get_current_active_user, oauth2_scheme
)

Base.metadata.create_all(bind=engine)

application = FastAPI(debug=True)


@application.get("/", include_in_schema=False)
def redirect_to_docs(request: Request) -> RedirectResponse:
    host_url = request.url.components.geturl() + "docs/"
    url = URL(host_url)
    return RedirectResponse(url)


@application.post("/token")
async def login(
    db: DataBaseDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = get_user(form_data.username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="wrong username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="wrong username or password")

    return {"access_token": user.email, "token_type": "bearer"}


@application.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@application.get("/tokens/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
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
