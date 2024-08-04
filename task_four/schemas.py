from pydantic import BaseModel, field_validator, Field, EmailStr
from datetime import datetime, timezone
from fastapi import HTTPException, status
from .util import str_to_datetime, date_to_str


class AuthorBookOut(BaseModel):
    id: int
    title: str
    genre: str
    ISBN: str
    publication_date: str

    class ConfigDict:
        from_attributes = True


class Borrow(BaseModel):
    user_id: int
    book_id: int
    return_date: str


class BorrowIn(Borrow):
    @field_validator("return_date")
    def validate_date_str(cls, date_str):
        try:
            return_date = str_to_datetime(date_str)
            date_now = datetime.now(timezone.utc)
            date_now_com = str_to_datetime(
                datetime.strftime(date_now, format="%d-%m-%Y")
            )
            if return_date <= date_now_com:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"The return date must be greater than today's date: {date_now_com.strftime('%d-%m-%Y')}",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": f"{str(e)}. Also, check to confirm the date entered corresponds with the specified format - dd-mm-yyyy."
                },
            )
        else:
            return date_str


class BorrowOut(Borrow):

    id: int
    borrow_date: str
    returned: bool

    class ConfigDict:
        from_attributes = True


class Book(BaseModel):
    author_id: int = Field(examples=[1])
    title: str = Field(examples=["Pride and Prejuice"])
    genre: str = Field(examples=["Romance"])
    ISBN: str = Field(examples=["978-3-16-148410-0"])
    publication_date: str = Field(examples=["15-03-2022"])


class BookIn(Book):
    @field_validator("publication_date")
    def validate_date_str(cls, date_str):
        try:
            str_to_datetime(date_str)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": f"{str(e)}. Check to confirm the date entered corresponds with the specified format - dd-mm-yyyy."
                },
            )
        else:
            return date_str


class BookOut(Book):
    id: int

    class ConfigDict:
        from_attributes = True


class User(BaseModel):
    name: str = Field(examples=["John Doe"])
    email: EmailStr = Field(examples=["john@email.com"])


class UserIn(User):
    password: str = Field(examples=["secret"], min_length=4)


class UserOut(User):
    id: int
    borrow_records: list[BorrowOut]

    class ConfigDict:
        from_attributes = True


class Author(BaseModel):
    name: str = Field(examples=["Jane Austine"])
    birthdate: str = Field(examples=["10-02-1962"])
    nationality: str = Field(examples=["England"])


class AuthorIn(Author):
    @field_validator("birthdate")
    def validate_date_str(cls, date_str):
        try:
            str_to_datetime(date_str)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": f"{str(e)}. Check to confirm the date entered corresponds with the specified format - dd-mm-yyyy."
                },
            )
        else:
            return date_str


class AuthorOut(Author):
    id: int
    books: list[AuthorBookOut]

    class ConfigDict:
        from_attributes = True
