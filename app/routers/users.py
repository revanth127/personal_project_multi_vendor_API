from fastapi import APIRouter,Depends,status
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
import app.schemas as schemas
from app.utils import hash_password 

router = APIRouter(
    prefix='/users'
)

@router.post('/register', response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)

    new_user = models.Users(
    email=user.email,
    hashed_password=hashed_password,
    role=user.role
)


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user