from fastapi import APIRouter,Depends,HTTPException,status
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import app.schemas as schemas
from app.oauth2 import get_current_user
from typing import Annotated


router = APIRouter(
    prefix='/sellers',
    tags= ['sellers']
)


db_dep = Annotated[Session, Depends(get_db)]
user_dep = Annotated[models.Users, Depends(get_current_user)]


class Context:
    def __init__(self, db: db_dep, user: user_dep):
        self.db = db
        self.user = user
MarketContext = Annotated[Context, Depends()]


def is_seller(ctx:MarketContext):
    if ctx.user.role != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can update products"
        )


@router.post('/create_product',status_code=status.HTTP_201_CREATED)
def create_product(product:schemas.ProductCreate,ctx: MarketContext):
    
    is_seller(ctx)
    
    new_product = models.Products(
        name = product.name,
        price = product.price,
        stock = product.quantity,
        owner_id=ctx.user.id   
    )
    try:
        ctx.db.add(new_product)
        ctx.db.commit()
        ctx.db.refresh(new_product)
    except SQLAlchemyError:
        ctx.db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


    return new_product

@router.put('/update_product/{product_id}')
def update_product(product_id:int,product_update:schemas.ProductUpdate,ctx: MarketContext):
    
    is_seller(ctx) 
    

    product = ctx.db.query(models.Products).filter(
        models.Products.id == product_id,
        models.Products.owner_id == ctx.user.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found or or unauthorized")
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    
    try:
        ctx.db.commit()
        ctx.db.refresh(product)
    except SQLAlchemyError:
            ctx.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    
    return {"status": "success", "message": f"{product_id} updated"}


@router.delete('/delete_product/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(ctx: MarketContext, product_id: int):
    is_seller(ctx)

    product_query = ctx.db.query(models.Products).filter(
        models.Products.id == product_id,
        models.Products.owner_id == ctx.user.id 
    )
    
    product = product_query.first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found or unauthorized"
        )
    
    try:
        product_query.delete(synchronize_session=False)
        ctx.db.commit()
    except SQLAlchemyError:
        ctx.db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred during deletion"
        )
    
    return None

@router.get('/my_products', response_model=list[schemas.ProductOut])
def view_my_products(
    ctx: MarketContext,
    status: str|None = None,
    min_price: str|None = None,
    max_price: str|None = None,
    low_stock_threshold: int = 5
):
    query = ctx.db.query(models.Products).filter(models.Products.owner_id == ctx.user.id)

    if status == "in_stock":
        query = query.filter(models.Products.stock > 0)
    elif status == "out_of_stock":
        query = query.filter(models.Products.stock == 0)
    elif status == "low_inventory":
        query = query.filter(models.Products.stock > 0, models.Products.stock <= low_stock_threshold)

    if min_price is not None:
        query = query.filter(models.Products.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Products.price <= max_price)

    return query.all()