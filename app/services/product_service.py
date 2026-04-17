from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.schemas import ProductCreate, ProductUpdate, BrowseProducts
from fastapi import HTTPException, status
from typing import List, Optional
from decimal import Decimal
import app.models as models

class ProductService:
    def __init__(self, db: Session):
        self.product_repo = ProductRepository(db)

    def create_product(self, product_data: ProductCreate, seller_id: int) -> models.Products:
        product = self.product_repo.create_product(
            name=product_data.name,
            price=Decimal(str(product_data.price)),
            stock=product_data.quantity,
            owner_id=seller_id
        )
        return product

    def get_product(self, product_id: int) -> models.Products | None:
        return self.product_repo.get(product_id)

    def update_product(
        self, 
        product_id: int, 
        product_update: ProductUpdate, 
        seller_id: int
    ) -> models.Products:
        product = self.product_repo.get_by_owner(seller_id, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or unauthorized"
            )
        
        update_data = product_update.model_dump(exclude_unset=True)
        # Handle field name mapping (quantity -> stock)
        if 'quantity' in update_data:
            update_data['stock'] = update_data.pop('quantity')
        
        return self.product_repo.update(product, update_data)

    def delete_product(self, product_id: int, seller_id: int) -> None:
        product = self.product_repo.get_by_owner(seller_id, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or unauthorized"
            )
        
        self.product_repo.delete(product_id)

    def get_products_with_filters(
        self,
        skip: int = 0,
        limit: int = 100,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        seller_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[models.Products]:
        return self.product_repo.get_filtered_products(
            skip=skip,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            seller_id=seller_id,
            search=search
        )

    def update_product_stock(self, product_id: int, new_stock: int) -> models.Products:
        product = self.product_repo.update_stock(product_id, new_stock)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product
