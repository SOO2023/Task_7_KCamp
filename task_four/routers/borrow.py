from fastapi import APIRouter, Depends, HTTPException, status, Form
from ..database import db_session
from sqlalchemy.orm import Session
from ..models import BorrowRecords, Books, Users
from ..schemas import BorrowIn, BorrowOut
from ..util import get_all_items, get_all_items, get_item_by_id, create_new_item
from ..authenticate import get_current_user


router = APIRouter(tags=["Borrow"])


@router.post(
    "/borrow/{book_id}",
    response_model=BorrowOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint is used to borrow a book, also verifying that the borrower already has an account and logged in.",
)
def borrow_book(
    book_id: int,
    return_date: str = Form(examples=["22-12-2024"]),
    db: Session = Depends(db_session),
    user_id: int = Depends(get_current_user),
):
    _ = get_item_by_id(book_id, db, Books, "book")
    user = get_item_by_id(user_id, db, Users, "user")
    if user.borrow_records:
        for borrow_book in user.borrow_records:
            if not borrow_book.returned and borrow_book.book_id == book_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "message": "You already borrowed the book with id and yet to return it. You can only borrow a book you have returned again."
                    },
                )
    borrow_info = BorrowIn(book_id=book_id, return_date=return_date, user_id=user_id)
    borrow = create_new_item(borrow_info.model_dump(), db, BorrowRecords)
    return borrow


@router.get(
    "/borrow/users/history",
    response_model=list[BorrowOut],
    status_code=status.HTTP_200_OK,
    description="This endpoint allows users to check their borrow history.",
)
def get_user_history(
    db: Session = Depends(db_session),
    user_id: int = Depends(get_current_user),
):
    borrow_history = get_all_items(db, BorrowRecords)
    user_borrow_history = [
        borrow for borrow in borrow_history if borrow.user_id == user_id
    ]
    return user_borrow_history


@router.post(
    "/return/{borrow_id}",
    response_model=BorrowOut,
    status_code=status.HTTP_200_OK,
    description="This endpoint allows user to return previously borrowed book.",
)
def return_book(
    borrow_id: int,
    db: Session = Depends(db_session),
    user_id: int = Depends(get_current_user),
):
    borrow = get_item_by_id(borrow_id, db, BorrowRecords, "borrow_record")
    if borrow.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "You have no such borrow record. Check borrow id and try again."
            },
        )
    if borrow.returned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": f"You have already returned this book with id {borrow.book_id}."
            },
        )
    borrow.returned = True
    db.commit()
    return borrow
