from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from datetime import datetime, timezone
from sqlalchemy import ForeignKey


class Posts(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)
    date_posted: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    comments: Mapped[list["Comments"]] = Relationship(
        backref="post",
        cascade="all, delete",
    )


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[list["Posts"]] = Relationship(
        backref="user",
        cascade="all, delete",
    )


class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(nullable=False)
    date_commented: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
