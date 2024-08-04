from fastapi import APIRouter, Depends, status
from ..database import db_session
from sqlalchemy.orm import Session
from ..schemas import AuthorIn, AuthorOut
from ..models import Authors
from ..util import (
    create_new_item,
    get_all_items,
    get_item_by_id,
    update_item,
    delete_item,
)

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post(
    "/",
    response_model=AuthorOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint add new author to the database.",
)
def add_author(author: AuthorIn, db: Session = Depends(db_session)):
    author = create_new_item(author.model_dump(), db, Authors)
    return author


@router.get(
    "/",
    response_model=list[AuthorOut],
    description="This endpoint queries all the authors in the database.",
)
def get_all_authors(db: Session = Depends(db_session)):
    authors = get_all_items(db, Authors)
    return authors


@router.get(
    "/{author_id}",
    response_model=AuthorOut,
    description="This endpoint is used to get specific author in the database.",
)
def get_author(author_id: int, db: Session = Depends(db_session)):
    author = get_item_by_id(author_id, db, Authors, "author")
    return author


@router.put(
    "/{author_id}",
    response_model=AuthorOut,
    description="This endpoint is used to update an author information.",
    status_code=status.HTTP_201_CREATED,
)
def update_author_info(
    author_id: int, author_info: AuthorIn, db: Session = Depends(db_session)
):
    author = update_item(author_id, author_info.model_dump(), db, Authors, "author")
    return author


@router.delete(
    "/{author_id}",
    description="This endpoint is used to delete an author from the database.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_author(author_id: int, db: Session = Depends(db_session)):
    delete_item(author_id, db, Authors, "author")
