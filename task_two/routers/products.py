from fastapi import APIRouter, Depends
from ..database import db_session
from sqlalchemy.orm import Session
from ..models import Products
from ..schemas import ProductIn, ProductOut
from ..util import create_new_item, get_all_items


router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductOut,
    description="This endpoint is used to add product into the database.",
)
def add_product(product: ProductIn, db: Session = Depends(db_session)):
    product = create_new_item(product.model_dump(), db, Products)
    return product


@router.get(
    "/",
    response_model=list[ProductOut],
    description="This endpoint is used to query all the products in the database.",
)
def get_all_products(db: Session = Depends(db_session)):
    products = get_all_items(db, Products)
    return products
