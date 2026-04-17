from sqlalchemy.orm import Session
from sqlalchemy import update
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository, OrderItemRepository
from app.schemas import OrderProduct
from fastapi import HTTPException, status
from typing import List
from decimal import Decimal
import app.models as models

class OrderService:
    def __init__(self, db: Session):
        self.product_repo = ProductRepository(db)
        self.order_repo = OrderRepository(db)
        self.order_item_repo = OrderItemRepository(db)

    def create_order(self, buyer_id: int, product_id: int, quantity: int) -> models.OrderItems:
        # Check product availability
        product = self.product_repo.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        if product.stock < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )
        
        # Atomic stock update
        stmt = (
            update(models.Products)
            .where(models.Products.id == product_id)
            .where(models.Products.stock >= quantity)
            .values(stock=models.Products.stock - quantity)
        )
        
        result = self.product_repo.db.execute(stmt)
        
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock (concurrent update)"
            )
        
        # Create order
        total_amount = product.price * quantity
        order = self.order_repo.create_order(
            user_id=buyer_id,
            total_amount=total_amount,
            status="pending"
        )
        
        # Create order item
        order_item = self.order_item_repo.create_order_item(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity,
            price_at_purchase=product.price
        )
        
        return order_item

    def update_order_status(self, order_id: int, new_status: str, user_id: int, user_role: str) -> models.Order:
        order = self.order_repo.get(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Validate status transition
        self._validate_status_transition(order.status, new_status, user_role)
        
        # Only buyer can cancel their own orders
        if new_status == "cancelled" and (order.user_id != user_id or user_role != "buyer"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only buyers can cancel their own orders"
            )
        
        return self.order_repo.update_status(order_id, new_status)

    def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Order]:
        return self.order_repo.get_user_orders(user_id, skip, limit)

    def get_order_items(self, order_id: int) -> List[models.OrderItems]:
        return self.order_item_repo.get_order_items(order_id)

    def _validate_status_transition(self, current_status: str, new_status: str, user_role: str) -> None:
        valid_transitions = {
            "pending": ["confirmed", "cancelled"],
            "confirmed": ["shipped"],
            "shipped": ["delivered"],
            "delivered": [],
            "cancelled": []
        }
        
        if new_status not in valid_transitions.get(current_status, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from {current_status} to {new_status}"
            )
        
        # Only sellers can confirm, ship, and mark as delivered
        if new_status in ["confirmed", "shipped", "delivered"] and user_role != "seller":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only sellers can update order status to confirmed, shipped, or delivered"
            )
