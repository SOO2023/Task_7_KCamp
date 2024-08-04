from fastapi import APIRouter, Depends, status
from ..util import create_new_item, get_all_items
from ..database import db_session
from sqlalchemy.orm import Session
from ..schemas import UserIn, UserOut
from ..models import Users
from ..authenticate import HashVerifyPassword

hash_verify_pwd = HashVerifyPassword()
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint allows a new user to create an account. Ensuring that username are unique to users and password characters are not less than 4.",
)
def create_user(user: UserIn, db: Session = Depends(db_session)):
    user.password = hash_verify_pwd.hash_password(user.password)
    user = create_new_item(user.model_dump(), db, Users)
    return user


@router.get(
    "/",
    response_model=list[UserOut],
    description="This endpoint queries all the user in the database.",
)
def get_all_users(db: Session = Depends(db_session)):
    users = get_all_items(db, Users)
    return users
