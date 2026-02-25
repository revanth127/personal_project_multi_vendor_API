from app.database import Base
from sqlalchemy import TIMESTAMP, Column,Integer,Numeric,String,text,ForeignKey,Enum,UniqueConstraint

#--------------
#Identity & Roles
#---------------

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True,index=True)
    hashed_password = Column(String,nullable=False)
    role = Column(Enum('buyer', 'seller', name='user_roles'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)

#--------------
#The Items for Sale
#--------------
class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    price = Column(Numeric(10,2),nullable=False)
    stock = Column(Integer,nullable=False)
    owner_id = Column(ForeignKey('users.id',ondelete='CASCADE'),nullable=False,index=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)

    __table_args__=(
        UniqueConstraint('name','owner_id',name='_customer_prooduct_uc'),
    )

#--------------
#The Transaction
#---------------

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False,index=True) #Buyer
    total_amount = Column(Numeric(10,2),nullable=False)
    status = Column(Enum(
    "pending",
    "paid",
    "shipped",
    "delivered",
    "cancelled",
    name="order_status"
), nullable=False, server_default="pending")
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)
    

#--------------
#The specific items in an order
#---------------

class OrderItems(Base):
    __tablename__ = 'orderitems'

    id = Column(Integer,primary_key=True,nullable=False)
    order_id = Column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False,index=True)
    product_id = Column(ForeignKey('products.id',ondelete='CASCADE'),nullable=False,index=True)
    quantity = Column(Integer, nullable=False, default=1)
    price_at_purchase = Column(Numeric(10,2),nullable=False)

