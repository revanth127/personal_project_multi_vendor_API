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


#-----------------
#Output for browsing products
#-----------------


class BrowseProducts(BaseModel):
    id: int
    name: str
    price : int
    stock_available : int

    class Config:
        from_attributes = True

#-----------------
#input for creating a product in sellers.py
#-----------------

class ProductCreate(BaseModel):
    name : str
    quantity : int
    price : int

