from fastapi import APIRouter,Depends,HTTPException,status
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import app.schemas as schemas
from typing import Annotated,List

router = APIRouter(
    prefix='/buyers',
    tags = ['buyers']
)

db_dep = Annotated[Session, Depends(get_db)]

@router.get('/browse_products',response_model=List[schemas.BrowseProducts])
def browse_products(db: db_dep,limits:int = 15,search:str|None = None):
    try:
        products = db.query(models.Products).filter(models.Products.name.icontains(search)).limit(limits).all()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'cannot find {search}')
    
    return products 





