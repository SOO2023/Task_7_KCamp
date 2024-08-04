from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from datetime import datetime, timezone
from sqlalchemy import ForeignKey
import random


class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    unit_price: Mapped[float] = mapped_column(nullable=False)
    available_quantity: Mapped[int] = mapped_column(nullable=False)
    available: Mapped[bool] = mapped_column(default=True)


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    contact: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str]
    password: Mapped[str]
    orders: Mapped[list["Orders"]] = Relationship(back_populates="user")


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(nullable=False)
    order_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    order_status: Mapped[str] = mapped_column(default="Pending")
    completion_time: Mapped[int] = mapped_column(default=lambda: random.randint(1, 3))
    user: Mapped["Users"] = Relationship(back_populates="orders")
