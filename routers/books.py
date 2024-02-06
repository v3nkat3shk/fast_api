from typing import Annotated, Generator, Any

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from database.database import get_db
from database import query, schemas
from utils.exceptions import UserNotFoundException

router = APIRouter()


DataBaseDep = Annotated[Generator[Session, Any, None], Depends(get_db)]


@router.post("/users/{user_id}/books/", response_model=schemas.Book)
def create_book_for_user(user_id: int, book: schemas.BookCreate, db: DataBaseDep):
    return query.create_user_book(db=db, book=book, user_id=user_id)


@router.get("/books/", response_model=list[schemas.Book])
def read_books(db: DataBaseDep, skip: int = 0, limit: int = 100):
    books = query.get_books(db, skip=skip, limit=limit)
    return books


@router.get("/books/{user_id}", response_model=list[schemas.Book])
def read_user_books(user_id: int, db: DataBaseDep, skip: int = 0, limit: int = 100):
    user = query.get_user(db, user_id=user_id)
    if not user:
        raise UserNotFoundException(user_id)

    return query.get_users_books(db, user)
