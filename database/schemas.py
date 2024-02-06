from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    description: str | None = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    created_by_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "book",
                    "title": "book title",
                    "description": "book description",
                    "created_by_id": "user_id",
                }
            ]
        }
    )


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    books: list[Book] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 0,
                    "email": "testemail@email.com",
                    "is_acitve": False,
                    "books": [
                        {
                            "id": 1,
                            "title": "book title",
                            "description": "book description",
                            "created_by_id": 0,
                        },
                    ]
                }
            ]
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
