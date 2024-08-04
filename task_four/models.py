from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from .util import date_to_str
from sqlalchemy import ForeignKey


class Books(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    ISBN: Mapped[str] = mapped_column(nullable=False)
    publication_date: Mapped[str] = mapped_column()
    borrow_records: Mapped[list["BorrowRecords"]] = Relationship(
        backref="book", cascade="all, delete"
    )


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    borrow_records: Mapped[list["BorrowRecords"]] = Relationship(
        backref="user", cascade="all, delete"
    )


class Authors(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birthdate: Mapped[str] = mapped_column(nullable=False)
    nationality: Mapped[str] = mapped_column(nullable=False)
    books: Mapped[list["Books"]] = Relationship(backref="author", cascade="all, delete")


class BorrowRecords(Base):
    __tablename__ = "borrow_records"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    borrow_date: Mapped[str] = mapped_column(default=date_to_str)
    return_date: Mapped[str] = mapped_column()
    returned: Mapped[bool] = mapped_column(default=False)
