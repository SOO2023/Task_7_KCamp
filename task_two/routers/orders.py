from fastapi import APIRouter, Depends, HTTPException, status, Form
from ..authenticate import JWT, verify_user, get_current_user
from ..database import db_session
from sqlalchemy.orm import Session
from ..models import Orders, Users, Products
from ..schemas import OrderIn, OrderOut
from ..util import *
import threading

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get(
    "/{order_id}",
    response_model=OrderOut,
    description="This endpoints allows authenticated user to query their order by order id",
)
def get_order_by_id(
    order_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    order = get_item_by_id(order_id, db, Orders, "order")
    if order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"No such order with id {order_id} can be found in your order history."
            },
        )
    else:
        order_dict = order_out(order, order.product_id, db)
        return order_dict


@router.get(
    "/",
    response_model=list[OrderOut],
    description="This endpoint allows the user to query all orders.",
)
def get_all_orders(
    user_id: int = Depends(get_current_user), db: Session = Depends(db_session)
):
    user = db.query(Users).filter(Users.id == user_id).first()
    user_orders = user.orders
    if user_orders:
        user_orders = [order_out(order, order.product_id, db) for order in user_orders]
    return user_orders


@router.post(
    "/",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint allows user to order product with product id.",
)
def make_order(
    product_id: int = Form(examples=[1]),
    quantity: int = Form(gt=0, examples=[5]),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    order = OrderIn(product_id=product_id, quantity=quantity)
    product = get_item_by_id(order.product_id, db, Products, "product")
    verify_and_update_order(product=product, quantity=order.quantity, db=db)
    order.product_id
    total_price = order.quantity * product.unit_price
    order_dict = order.model_dump()
    order_dict.update(
        {
            "user_id": user_id,
            "unit_price": product.unit_price,
            "total_price": total_price,
        }
    )
    order = create_new_item(order_dict, db, Orders)
    thread = threading.Thread(
        target=lambda: background_complete_status(id=order.id, db=db)
    )
    thread.start()
    order_dict_out = order_out(order, order.product_id, db)
    return order_dict_out


@router.put(
    "/{order_id}",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint will allow the user to edit their previous orders.",
)
def update_orders(
    order_id: int,
    user_id: int = Depends(get_current_user),
    quantity: int = Form(gt=0),
    db: Session = Depends(db_session),
):

    order_dict_out = verify_and_update_order(
        quantity=quantity, db=db, order_id=order_id, user_id=user_id, post=False
    )
    return order_dict_out


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="This endpoint will allow the user to delete their previous orders.",
)
def delete_orders(
    order_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    verify_and_update_order(
        quantity=0, db=db, order_id=order_id, user_id=user_id, post=False, delete=True
    )
