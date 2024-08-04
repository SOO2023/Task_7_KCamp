from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy_to_pydantic import sqlalchemy_to_pydantic
from .models import Orders, Products
import time, os
from secrets import token_hex
from PIL import Image
import math


# CRUD
def get_item_by_id(id: int, db: Session, Model, item_name: str = "item"):
    item = db.query(Model).filter(Model.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"{item_name.capitalize()} with id {id} cannot be found."
            },
        )
    return item


def get_all_items(db: Session, Model):
    items = db.query(Model).all()
    return items


def create_new_item(item_dict: dict, db: Session, Model):
    try:
        item = Model(**item_dict)
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        )
    else:
        return item


def delete_item(id: int, db: Session, Model, item_name: str = "item"):
    get_item_by_id(id, db, Model, item_name)
    item = db.query(Model).filter(Model.id == id).first()
    db.delete(item)
    db.commit()


def update_item(
    id: int, update_dict: dict, db: Session, Model, item_name: str = "item"
):
    get_item_by_id(id, db, Model, item_name)
    item = db.query(Model).filter(Model.id == id)
    try:
        item.update(update_dict)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        )
    else:
        return item.first()


# BACKGROUND TASK FUNCTION
def background_complete_status(id: int, db: Session):
    order = db.query(Orders).filter(Orders.id == id)
    seconds = 60 * order.first().completion_time
    time.sleep(seconds)
    order.update({"order_status": "Completed"})
    db.commit()


# VERIFYING USER ORDER
def verify_and_update_order(
    quantity: int,
    db: Session,
    product: Products | None = None,
    order_id: int | None = None,
    user_id: int | None = None,
    post: bool = True,
    delete: bool = False,
) -> dict | None:
    if post:
        if not product.available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": f"The product is currently not avaialable. Check back some time later."
                },
            )
        available_quantity = product.available_quantity
        if available_quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": f"The available quantity for this product is {available_quantity}"
                },
            )
        product.available_quantity -= quantity
        db.commit()
    # update
    else:
        order = get_item_by_id(order_id, db, Orders, "order")
        product = get_item_by_id(order.product_id, db, Products, "product")
        if order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": f"You do not have any order with the id {order_id}."
                },
            )

        initial_prod_qty = product.available_quantity + order.quantity
        if quantity > initial_prod_qty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": f"The new quantity is more than the avaialble quantity ({initial_prod_qty})"
                },
            )
        product.available_quantity = initial_prod_qty
        if not delete:
            product.available_quantity -= quantity
            order.quantity = quantity
            order.total_price = quantity * order.unit_price
            db.commit()
        else:
            db.query(Orders).filter(Orders.id == order_id).delete()
            db.commit()
    if product.available_quantity == 0:
        product.available = False
        db.commit()
    if not post:
        if not delete:
            return order_out(order, order.product_id, db)


def sql_obj_to_pydantic(sql_obj, ModelClass) -> dict:
    PydanticObj = sqlalchemy_to_pydantic(ModelClass)
    pydantic_obj = PydanticObj.model_validate(sql_obj)
    return pydantic_obj.model_dump()


def order_out(order, product_id, db):
    order_dict = sql_obj_to_pydantic(order, Orders)
    prod_obj = get_item_by_id(product_id, db, Products)
    prod_dict = sql_obj_to_pydantic(prod_obj, Products)
    prod_dict_extracted = {
        "product_id": prod_dict["id"],
        "product_name": prod_dict["name"],
        "product_category": prod_dict["category"],
    }
    order_dict.update({"product_details": prod_dict_extracted})
    return order_dict


def home_page(
    title: str, assignment_desc: str, assignment_details: str, task_no: int
) -> str:
    home = f"""
    <!doctype html>
    <html>
    <head>
    <title>{title}</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    </head>
    <body class="bg-light">
    <div class="container bg-white shadow-sm border border-light rounded" style="margin-top: 80px; padding: 10px;">
    <div class="container text-secondary border-bottom" style="text-align:center;">
    <h1>Task 7 FastAPI Backend - Task {task_no}</h1>
    </div>
    <div class="container" style="margin-top: 30px; padding: 10px;">
    <h4 class="text-body">{assignment_desc}</h4>
    <p>{assignment_details}</p>
    </div>
    </div>
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return home
