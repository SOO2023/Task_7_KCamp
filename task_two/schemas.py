from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from .models import Users
from .database import sessionLocal
from fastapi import HTTPException, status


class Product(BaseModel):
    name: str
    category: str
    unit_price: float
    available_quantity: int
    available: bool


class ProductIn(Product):
    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "name": "Hisense 45 Inches TV",
                    "category": "Electronics",
                    "unit_price": 20.4,
                    "available_quantity": 102,
                    "available": True,
                }
            ]
        }


class ProductOut(Product):
    id: int

    class ConfigDict:
        from_attributes = True


class User(BaseModel):
    name: str
    address: str
    contact: str
    email: EmailStr


class UserIn(User):
    password: str

    @field_validator("email")
    def email_validator(cls, email):
        db = sessionLocal()
        user = db.query(Users).filter(Users.email == email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail={"message": "The email has already been used by another user."},
            )
        return email

    @field_validator("password")
    def password_validator(cls, pwd):
        if len(pwd) < 4:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail={"message": "Password should have at least 4 characters."},
            )
        return pwd

    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "name": "John Doe",
                    "address": "1 Abc Street",
                    "contact": "+234123456789",
                    "email": "johndoe@email.com",
                    "password": "secret1234",
                }
            ]
        }


class UserOut(User):
    id: int

    class ConfigDict:
        from_attributes = True


class Order(BaseModel):
    product_id: int
    quantity: int


class OrderIn(Order):
    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "product_id": 1,
                    "quantity": 5,
                }
            ]
        }


class OrderOut(Order):
    id: int
    user_id: int
    unit_price: float
    total_price: float
    order_date: datetime
    order_status: str
    completion_time: int
    product_details: dict

    class ConfigDict:
        from_attributes = True
