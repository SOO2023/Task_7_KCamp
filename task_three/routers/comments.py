from fastapi import APIRouter, Depends, HTTPException, status, Form
from ..database import db_session
from sqlalchemy.orm import Session
from ..models import Comments, Posts
from ..schemas import CommentIn, CommentOut
from ..util import get_all_items, get_all_items, get_item_by_id, create_new_item
from ..authenticate import get_current_user


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get(
    "/all-comments",
    response_model=list[CommentOut],
    description="This endpoint queries all the comments in the database.",
)
def get_all_comments(db: Session = Depends(db_session)):
    comments = get_all_items(db, Comments)
    return comments


@router.get(
    "/",
    response_model=list[CommentOut],
    description="This endpoint is used to query all user comments in the database.",
)
def get_all_user_comments(
    db: Session = Depends(db_session), user_id: int = Depends(get_current_user)
):
    comments = get_all_items(db, Comments)
    user_comments = [comment for comment in comments if comment.user_id == user_id]
    return user_comments


@router.get(
    "/{comment_id}",
    response_model=CommentOut,
    description="This endpoint is used to query a specific comment in the database.",
)
def get_user_comment(
    comment_id: int,
    db: Session = Depends(db_session),
    user_id: int = Depends(get_current_user),
):
    comment = get_item_by_id(comment_id, db, Comments, "comment")
    if comment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"The user does not have a comment with the id {comment_id}"
            },
        )
    return comment


@router.post(
    "/{post_id}",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint is used to comment on a post with the id 'post_id' which is then stored in the database.",
)
def comment_on_a_post(
    post_id: int,
    user_id: int = Depends(get_current_user),
    content: str = Form(),
    db: Session = Depends(db_session),
):
    _ = get_item_by_id(post_id, db, Posts, "post")
    comment = CommentIn(content=content, user_id=user_id, post_id=post_id)
    comment = create_new_item(comment.model_dump(), db, Comments)
    return comment


@router.put(
    "/{comment_id}",
    response_model=CommentOut,
    description="This endpoint allows the user to edit previous comment on a post.",
    status_code=status.HTTP_201_CREATED,
)
def edit_user_comment(
    comment_id: int,
    content: str = Form(),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    comment = get_item_by_id(comment_id, db, Comments, "comment")
    if comment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You cannot edit other user's comment."},
        )
    comment.content = content
    db.commit()
    return comment


@router.delete(
    "/{comment_id}",
    description="This endpoint allows the user to delete previous comment.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_comment(
    comment_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    comment = get_item_by_id(comment_id, db, Comments, "comment")
    if comment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": f"You cannot delete other user's comment."},
        )
    db.delete(comment)
    db.commit()
