from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.product_service import ProductService
from app.middleware.auth import SellerUser, CurrentUser
from app.schemas import ProductCreate, ProductUpdate, BrowseProducts
from typing import List, Optional
from decimal import Decimal

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=BrowseProducts, status_code=201)
def create_product(
    product_data: ProductCreate,
    current_user: SellerUser = Depends(),
    db: Session = Depends(get_db)
):
    product_service = ProductService(db)
    return product_service.create_product(product_data, current_user.id)

@router.get("/", response_model=List[BrowseProducts])
def browse_products(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=15, ge=1, le=100),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    seller_id: Optional[int] = Query(default=None, ge=1),
    search: Optional[str] = Query(default=None),
    db: Session = Depends(get_db)
):
    product_service = ProductService(db)
    
    # Convert float to Decimal for precision
    min_price_decimal = Decimal(str(min_price)) if min_price is not None else None
    max_price_decimal = Decimal(str(max_price)) if max_price is not None else None
    
    return product_service.get_products_with_filters(
        skip=skip,
        limit=limit,
        min_price=min_price_decimal,
        max_price=max_price_decimal,
        seller_id=seller_id,
        search=search
    )

@router.put("/{product_id}")
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: SellerUser = Depends(),
    db: Session = Depends(get_db)
):
    product_service = ProductService(db)
    product_service.update_product(product_id, product_update, current_user.id)
    return {"status": "success", "message": f"Product {product_id} updated"}

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    current_user: SellerUser = Depends(),
    db: Session = Depends(get_db)
):
    product_service = ProductService(db)
    product_service.delete_product(product_id, current_user.id)
