from fastapi import APIRouter,Depends,HTTPException,status
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
import app.schemas as schemas
from app.oauth2 import get_current_user
from typing import Optional 

router = APIRouter(
    prefix='/sellers'
)

@router.post('/create_product')
def create_product(product:schemas.ProductCreate,db: Session = Depends(get_db),current_user : int = Depends(get_current_user)):
    
    if current_user.role != 'seller':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only sellers can create products"
        )
    
    new_product = models.Products(
        name = product.name,
        price = product.price,
        stock = product.quantity,
        owner_id=current_user.id   
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.put('/update_product')
def update_product(product_name:str,product_update:schemas.ProductUpdate,db: Session = Depends(get_db),current_user : int = Depends(get_current_user),search:Optional[str] = ''):
     
    product_query = db.query(models.Products).filter(
        models.Products.name == product_name,
        models.Products.owner_id == current_user.id
    )

    existing_product = product_query.first()

    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'there is no product named - {product_name}')
    
    product_query.update(product_update.model_dump(exclude_unset=True))
    db.commit()

    updated_product = product_query.first()

    return {'message':'product updated',
            'product' : updated_product}
    
     