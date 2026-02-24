from fastapi import APIRouter,Depends,HTTPException,status
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
import app.schemas as schemas
from typing import Optional,List

router = APIRouter(
    prefix='/buyers'
)

@router.get('/browse_products',response_model=List[schemas.BrowseProducts])
def browse_products(db: Session = Depends(get_db),limits:int = 15,search:Optional[str] =''):
    products = db.query(models.Products).filter(models.Products.name.icontains(search)).limit(limits).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'cannot find {search}')
    
    return products 





