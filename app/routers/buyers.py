from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy import update
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import SQLAlchemyError
import app.schemas as schemas
from typing import Annotated,List
from app.oauth2 import get_current_user

router = APIRouter(
    prefix='/buyers',
    tags = ['buyers']
)

db_dep = Annotated[Session, Depends(get_db)]
user_dep = Annotated[models.Users, Depends(get_current_user)]

class Context:
    def __init__(self, db: db_dep, user: user_dep):
        self.db = db
        self.user = user
MarketContext = Annotated[Context, Depends()]

@router.get('/browse_products',response_model=List[schemas.BrowseProducts])
def browse_products(ctx:MarketContext,limits: int = Query(default=15, ge=1, le=100),search : str|None = None):
    try:
        products = ctx.db.query(models.Products).filter(models.Products.name.icontains(search)).limit(limits).all()
    except SQLAlchemyError:
        ctx.db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'cannot find {search}')
    
    return products

#-------------------------
#Atomic update
#-------------------------

@router.post('/buy_product')
def buy_product(ctx:MarketContext,product_id:int,quantity:int = Query(ge=1)):

    if ctx.user.role != 'buyer':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only buyers can place orders'
        )
    
    product = ctx.db.query(models.Products).filter(models.Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    if product.stock < quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Insufficient stock')
  
    stmt = (
        update(models.Products)
        .where(models.Products.id == product_id)
        .where(models.Products.stock >= quantity)
        .values(stock = models.Products.stock - quantity)
    )
    
    try:
        result: CursorResult = ctx.db.execute(stmt)
        ctx.db.commit()
    except SQLAlchemyError:
        ctx.db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Insufficient stock'
        )

    return {"message": "Order placed successfully"}
        




