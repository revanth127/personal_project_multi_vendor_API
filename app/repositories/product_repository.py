from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.repositories.base import BaseRepository
import app.models as models
from typing import List, Optional
from decimal import Decimal

class ProductRepository(BaseRepository[models.Products]):
    def __init__(self, db: Session):
        super().__init__(models.Products, db)

    def get_by_owner(self, owner_id: int, product_id: int) -> Optional[models.Products]:
        return self.db.query(models.Products).filter(
            and_(
                models.Products.id == product_id,
                models.Products.owner_id == owner_id
            )
        ).first()

    def get_filtered_products(
        self,
        skip: int = 0,
        limit: int = 100,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        seller_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[models.Products]:
        query = self.db.query(models.Products)
        
        if min_price is not None:
            query = query.filter(models.Products.price >= min_price)
        
        if max_price is not None:
            query = query.filter(models.Products.price <= max_price)
        
        if seller_id is not None:
            query = query.filter(models.Products.owner_id == seller_id)
        
        if search:
            query = query.filter(models.Products.name.ilike(f"%{search}%"))
        
        return query.offset(skip).limit(limit).all()

    def create_product(
        self, 
        name: str, 
        price: Decimal, 
        stock: int, 
        owner_id: int
    ) -> models.Products:
        product_data = {
            "name": name,
            "price": price,
            "stock": stock,
            "owner_id": owner_id
        }
        return self.create(product_data)

    def update_stock(self, product_id: int, new_stock: int) -> Optional[models.Products]:
        product = self.get(product_id)
        if product:
            self.update(product, {"stock": new_stock})
        return product
