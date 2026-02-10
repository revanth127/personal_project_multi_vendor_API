from pydantic import BaseModel,EmailStr
from enum import Enum

#----------------
#for restricting roles to only buyers or sellers
#----------------

class UserRole(str, Enum):
    buyer = "buyer"
    seller = "seller"

#----------------
#for creating new users
#----------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

#----------------
#response, after creating the user
#----------------

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

