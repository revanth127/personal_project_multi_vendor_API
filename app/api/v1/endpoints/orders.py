from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.order_service import OrderService
from app.middleware.auth import BuyerUser, CurrentUser,require_buyer,require_seller,get_current_user
from app.schemas import OrderProduct
from typing import List
import app.models as models

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/buy/{product_id}", response_model=OrderProduct)
def buy_product(
    product_id: int,
    quantity: int = Query(default=1, ge=1),
    current_user: models.Users = Depends(require_buyer),
    db: Session = Depends(get_db)
):
    order_service = OrderService(db)
    return order_service.create_order(current_user.id, product_id, quantity)

@router.get("/")
def get_my_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=15, ge=1, le=100),
    current_user: models.Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order_service = OrderService(db)
    return order_service.get_user_orders(current_user.id, skip, limit)

@router.get("/{order_id}/items")
def get_order_items(
    order_id: int,
    # current_user: CurrentUser = Depends(),
    db: Session = Depends(get_db)
):
    order_service = OrderService(db)
    return order_service.get_order_items(order_id)

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    new_status: str,
    current_user: models.Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order_service = OrderService(db)
    order_service.update_order_status(order_id, new_status, current_user.id, current_user.role)
    return {"status": "success", "message": f"Order {order_id} status updated to {new_status}"}
