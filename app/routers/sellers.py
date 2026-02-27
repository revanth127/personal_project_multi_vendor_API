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


@router.post('/create_product',status_code=status.HTTP_201_CREATED)
def create_product(product:schemas.ProductCreate,ctx: MarketContext):
    
    if ctx.user.role != 'seller':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only sellers can create products"
        )
    
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
def update_product(product_id:int,product_update:schemas.ProductUpdate,ctx: MarketContext,search: str | None = ''):
    
    if ctx.user.role != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can update products"
        ) 
    

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

#-------------------------
#to-do:needes to be tested
#-------------------------

@router.delete('/delete_product/{product_id}')
def delete_product(ctx:MarketContext,product_id:int,):

    product_query = ctx.db.query(models.Products).filter(models.Products.id == product_id)
    product = product_query.first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
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