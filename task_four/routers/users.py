from fastapi import APIRouter, Depends, status
from ..database import db_session
from sqlalchemy.orm import Session
from ..schemas import UserIn, UserOut
from ..models import Users
from ..authenticate import HashVerifyPassword
from ..util import (
    create_new_item,
    get_all_items,
    update_item,
    delete_item,
    get_item_by_id,
)

hash_password = HashVerifyPassword()
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint add new user to the database.",
)
def add_user(user: UserIn, db: Session = Depends(db_session)):
    user.password = hash_password.hash_password(user.password)
    user = create_new_item(user.model_dump(), db, Users)
    return user


@router.get(
    "/",
    response_model=list[UserOut],
    description="This endpoint queries all the users in the database.",
)
def get_all_users(db: Session = Depends(db_session)):
    users = get_all_items(db, Users)
    return users


@router.get(
    "/{user_id}",
    response_model=UserOut,
    description="This endpoint is used to get specific user in the database.",
)
def get_user(user_id: int, db: Session = Depends(db_session)):
    user = get_item_by_id(user_id, db, Users, "user")
    return user


@router.put(
    "/{user_id}",
    response_model=UserOut,
    description="This endpoint is used to update an user information.",
    status_code=status.HTTP_201_CREATED,
)
def update_user_info(
    user_id: int, user_info: UserIn, db: Session = Depends(db_session)
):
    user_info.password = hash_password.hash_password(user_info.password)
    user = update_item(user_id, user_info.model_dump(), db, Users, "user")
    return user


@router.delete(
    "/{user_id}",
    description="This endpoint is used to delete an user from the database.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(user_id: int, db: Session = Depends(db_session)):
    delete_item(user_id, db, Users, "user")
