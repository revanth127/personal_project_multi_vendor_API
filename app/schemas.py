from pydantic import BaseModel,EmailStr,ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


#-----------------
#Output for browsing products
#-----------------

class BrowseProducts(BaseModel):
    id: int
    name: str
    price : int
    stock : int

    model_config = ConfigDict(from_attributes=True)

#-----------------
#Output for buying product(buy_product) in buyers.py
#-----------------

class OrderProduct(BaseModel):
    id : int
    order_id : int
    product_id : int
    name : str
    price_at_purchase : int


#-----------------
#input for creating a product in sellers.py in product table
#-----------------

class ProductCreate(BaseModel):
    name : str
    quantity : int
    price : int

#-----------------
#updating a existing product in sellers.py in product table
#-----------------

class ProductUpdate(BaseModel):
    name : str
    quantity : int|None = None
    price : int

#-----------------
#Output for viewing seller products in sellers.py
#-----------------
class ProductOut(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

