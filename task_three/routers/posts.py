from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from ..database import db_session
from sqlalchemy.orm import Session
from ..models import Posts
from ..schemas import PostIn, PostOut
from ..util import *
from ..authenticate import get_current_user
import os


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/all-posts", response_model=list[PostOut])
def get_all_posts(db: Session = Depends(db_session)):
    posts = get_all_items(db, Posts)
    return posts


@router.get(
    "/",
    response_model=list[PostOut],
    description="This endpoint is used to query all the user posts in the database.",
)
def get_all_user_posts(
    db: Session = Depends(db_session), user_id: int = Depends(get_current_user)
):
    posts = get_all_items(db, Posts)
    user_posts = [post for post in posts if post.user_id == user_id]
    return user_posts


@router.get(
    "/{post_id}",
    response_model=PostOut,
    description="This endpoint is used to query a specific user post in the database.",
    dependencies=[Depends(get_current_user)],
)
def get_a_post(
    post_id: int,
    db: Session = Depends(db_session),
):
    post = get_item_by_id(post_id, db, Posts, "post")
    return post


@router.post(
    "/",
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint is used to create a user post which is stored in the database.",
)
def create_post(
    title: str = Form(),
    content: str = Form(),
    image: UploadFile = File(None),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    post = PostIn(title=title, content=content, user_id=user_id, image=None)
    if image:
        image_path = image_to_path(image=image)
        post.image = image_path
    post = create_new_item(post.model_dump(), db, Posts)
    return post


@router.put(
    "/{post_id}",
    response_model=PostOut,
    description="This endpoint allows the user to edit previous post.",
    status_code=status.HTTP_201_CREATED,
)
def edit_user_post(
    post_id: int,
    title: str = Form(),
    content: str = Form(),
    image: UploadFile = File(None),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    post = get_item_by_id(post_id, db, Posts, "post")
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": f"You can't edit other user's post"},
        )
    post.title = title
    post.content = content
    if image:
        if post.image:
            try:
                os.remove(post.image)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)}
                )
        image_path = image_to_path(image)
        post.image = image_path
    db.commit()
    return post


@router.delete(
    "/{post_id}",
    description="This endpoint allows the user to delete previous post.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_post(
    post_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    post = get_item_by_id(post_id, db, Posts, "post")
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": f"You can't delete other user's post"},
        )
    image_path = post.image
    if image_path:
        try:
            os.remove(image_path)
        except:
            pass
    db.delete(post)
    db.commit()
