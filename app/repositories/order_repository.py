from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.repositories.base import BaseRepository
import app.models as models
from typing import List, Optional
from decimal import Decimal

class OrderRepository(BaseRepository[models.Order]):
    def __init__(self, db: Session):
        super().__init__(models.Order, db)

    def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Order]:
        return self.get_multi(skip=skip, limit=limit, user_id=user_id)

    def create_order(self, user_id: int, total_amount: Decimal, status: str = "pending") -> models.Order:
        order_data = {
            "user_id": user_id,
            "total_amount": total_amount,
            "status": status
        }
        return self.create(order_data)

    def update_status(self, order_id: int, new_status: str) -> Optional[models.Order]:
        order = self.get(order_id)
        if order:
            self.update(order, {"status": new_status})
        return order

class OrderItemRepository(BaseRepository[models.OrderItems]):
    def __init__(self, db: Session):
        super().__init__(models.OrderItems, db)

    def create_order_item(
        self, 
        order_id: int, 
        product_id: int, 
        quantity: int, 
        price_at_purchase: Decimal
    ) -> models.OrderItems:
        item_data = {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "price_at_purchase": price_at_purchase
        }
        return self.create(item_data)

    def get_order_items(self, order_id: int) -> List[models.OrderItems]:
        return self.get_multi(order_id=order_id)
