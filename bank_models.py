from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    User_name = Column(String(50))
    email_id = Column(String(50))
    password = Column(String(10))
class Bank(Base):
    __tablename__ = "banking"
    bank_id = Column(Integer, primary_key=True, autoincrement=True, index = True)
    account_number = Column(Integer,autoincrement=True)
    mobile_number = Column(String(20))
    Name = Column(String(20))
    account_type = Column(String(10))
    email_id = Column(String(30))
    Address = Column(String(40))
    pin = Column(String(10))
    balance = Column(Float)