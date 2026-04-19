
from pydantic import BaseModel,EmailStr,ConfigDict
from enum import Enum

from pydantic import BaseModel,EmailStr, Field
from enum import Enum
from typing import Optional, List
from decimal import Decimal


#----------------
#for restricting roles to only buyers or sellers
#----------------

class UserRole(str, Enum):
    buyer = "buyer"
    seller = "seller"

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

#----------------
#for creating new users
#----------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
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
    price: Decimal
    stock: int

    model_config = ConfigDict(from_attributes=True)

#-----------------
#Output for buying product(buy_product) in buyers.py
#-----------------

class OrderProduct(BaseModel):
    id: int
    order_id: int
    product_id: int
    name: str
    price_at_purchase: Decimal
    quantity: int

    model_config = ConfigDict(from_attributes=True)

#-----------------
#input for creating a product in sellers.py in product table
#-----------------

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0)

#-----------------
#updating a existing product in sellers.py in product table
#-----------------

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)


# -----------------
# Output for viewing seller products in sellers.py
# -----------------

class ProductOut(ProductCreate):
    model_config = ConfigDict(from_attributes=True)


# -----------------
# Order schemas
# -----------------

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal

    model_config = ConfigDict(from_attributes=True)