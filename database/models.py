from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    books = relationship("Book", back_populates="created_by")

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, is_active={self.is_active})"



class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))

    created_by = relationship("User", back_populates="books")
