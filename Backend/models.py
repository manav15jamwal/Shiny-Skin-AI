from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean,Float
from datetime import datetime , timezone
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,index=True,primary_key=True)
    user_name = Column(String,index=True,nullable=False)
    hashed_password = Column(String,index=True,nullable=False)
    email = Column(String,index=True,unique=True)
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    predictions = relationship("Prediction",back_populates="user",cascade="all,delete")
    history = relationship("ChatHistory",back_populates="user",cascade="all,delete")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer,index=True,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    acne = Column(String,index=True,nullable=False)
    confidence = Column(Float,index=True)
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    user =  relationship("User",back_populates="predictions")

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    type = Column(String, nullable=False)
    usage_time = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)
    
class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),index=True)
    message = Column(String,nullable = False)
    response = Column(String,nullable = False)
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    user =  relationship("User",back_populates="history")
