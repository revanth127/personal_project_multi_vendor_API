from fastapi import APIRouter,Depends,HTTPException,status
import app.models as models
from app.oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import verify_password
from app.database import get_db

router = APIRouter()

@router.post('/login',status_code=status.HTTP_200_OK)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid Credentials")
    
    if not verify_password(user_credentials.password,user.hashed_password):
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid Credentials")
    
    access_token = create_access_token(user_id=user.id,role=user.role)
    return {"access_token":access_token,"token_type":"bearer"}