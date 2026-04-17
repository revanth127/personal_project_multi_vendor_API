from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.oauth2 import verify_access_token
from app.database import get_db
from sqlalchemy.orm import Session
import app.models as models
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> models.Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token_data["user_id"]).first()
    
    if user is None:
        raise credentials_exception
    
    return user

def require_role(required_role: str):
    def role_checker(current_user: models.Users = Depends(get_current_user)) -> models.Users:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. {required_role.title()} role required."
            )
        return current_user
    return role_checker

# Role dependencies
require_seller = require_role("seller")
require_buyer = require_role("buyer")

# Type annotations for better IDE support
CurrentUser = Annotated[models.Users, Depends(get_current_user)]
SellerUser = Annotated[models.Users, Depends(require_seller)]
BuyerUser = Annotated[models.Users, Depends(require_buyer)]
