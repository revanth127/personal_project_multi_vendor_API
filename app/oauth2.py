from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.config import settings
import app.models as models

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(user_id:int,role:str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "role" : role,
        "user_id" : user_id,
        "exp" : expire
    }

    encoded = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return encoded

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        role = payload.get("role")

        if user_id is None or role is None:
            raise credentials_exception

        return {
            "user_id": user_id,
            "role": role
        }

    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"} 
    )
    
    # 1. Decode and verify the token (returns the payload/id)
    token_data = verify_access_token(token, credentials_exception)
    
    # 2. Fetch the actual user from the DB
    user = db.query(models.Users).filter(models.Users.id == token_data["user_id"]).first()
    
    if user is None:
        raise credentials_exception
        
    return user # Now returns the full SQLAlchemy model instance