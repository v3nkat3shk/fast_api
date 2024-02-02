from sqlalchemy.orm import Session

import database.models as models
import database.schemas as schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()



def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_users_books(db: Session, user: schemas.User, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(models.Book.created_by==user)


def create_user_book(db: Session, book: schemas.BookCreate, user_id: int):
    db_book = models.Book(**book.model_dump(), created_by_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def hash_password(password: str) -> str:
    return password
