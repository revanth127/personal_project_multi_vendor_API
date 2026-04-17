from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.utils import hash_password, verify_password
from app.oauth2 import create_access_token
from app.schemas import UserCreate, UserResponse
from fastapi import HTTPException, status
import app.models as models

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = hash_password(user_data.password)
        user = self.user_repo.create_user(
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )
        
        return UserResponse(id=user.id, email=user.email, role=user.role)

    def authenticate_user(self, email: str, password: str) -> dict:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        access_token = create_access_token(user_id=user.id, role=user.role)
        return {"access_token": access_token, "token_type": "bearer"}

    def get_user_by_id(self, user_id: int) -> models.Users | None:
        return self.user_repo.get(user_id)
