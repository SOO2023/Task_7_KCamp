from fastapi import APIRouter, Depends, status, HTTPException
from ..database import db_session
from sqlalchemy.orm import Session
from ..schemas import BookIn, BookOut
from ..models import Books, Authors
from ..util import (
    create_new_item,
    get_all_items,
    get_item_by_id,
    update_item,
    delete_item,
)

router = APIRouter(prefix="/books", tags=["Books"])


@router.post(
    "/",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint add new book to the database.",
)
def add_book(book: BookIn, db: Session = Depends(db_session)):
    try:
        _ = get_item_by_id(book.author_id, db, Authors, "author")
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "The author id entered is invalid. Check and try again."
            },
        )
    book = create_new_item(book.model_dump(), db, Books)
    return book


@router.get(
    "/",
    response_model=list[BookOut],
    description="This endpoint queries all the books in the database.",
)
def get_all_books(db: Session = Depends(db_session)):
    books = get_all_items(db, Books)
    return books


@router.get(
    "/{book_id}",
    response_model=BookOut,
    description="This endpoint is used to get specific book in the database.",
)
def get_book(book_id: int, db: Session = Depends(db_session)):
    book = get_item_by_id(book_id, db, Books, "book")
    return book


@router.put(
    "/{book_id}",
    response_model=BookOut,
    description="This endpoint is used to update an book information.",
    status_code=status.HTTP_201_CREATED,
)
def update_book_info(
    book_id: int, book_info: BookIn, db: Session = Depends(db_session)
):
    book = update_item(book_id, book_info.model_dump(), db, Books, "book")
    return book


@router.delete(
    "/{book_id}",
    description="This endpoint is used to delete an book from the database.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_id: int, db: Session = Depends(db_session)):
    delete_item(book_id, db, Books, "book")
