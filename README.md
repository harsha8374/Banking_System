# Banking_System
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Transaction
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import engine,SessionLocal
from app.models import bank_models


app = FastAPI()

bank_models.Base.metadata.create_all(bind = engine)


class register(BaseModel):
    User_name: str
    email_id: str
    password : str

class registerResponse(BaseModel):
    User_name : str
    email_id : str
    password : str

class login(BaseModel):
    email_id : str
    password: str

class loginResponse(BaseModel):
    message: str
    user_id:int

class bank(BaseModel):
    account_number : int
    mobile_number : str
    Name : str
    account_type : str
    email_id : str
    Address : str
    class Config:
        orm_mode = True

class bankResponse(bank):
    bank_id : int

class pin_generate(BaseModel):
    account_number: int
    mobile_number: str
    pin: str
    confirm_pin: str

class pinResponse(BaseModel):
    bank_id : int

class depositRequest(BaseModel):
    Account_number: int
    amount:float
    pin:str

class depositResponse(BaseModel):
    account_number: int
    balance: float

    class Config:
        orm_mode: True

class Withdraw_request(BaseModel):
    account_number:int
    pin:str
    amount : int

class withdrawResponse(BaseModel):
    account_number:int
    pin:str
    balance:float

    class config:
        orm_mode:True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/register/", response_model=registerResponse, status_code=status.HTTP_201_CREATED)
def register(Register: register, db:db_dependency):
    db_user = db.query(bank_models.User).filter(bank_models.User.email_id == Register.email_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="email_id is already existed")
    new_user = bank_models.User(User_name= Register.User_name, email_id = Register.email_id, password = Register.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=loginResponse, status_code=status.HTTP_200_OK)
def login(Login:login, db:db_dependency):
    db_login = db.query(bank_models.User).filter(bank_models.User.email_id == Login.email_id, bank_models.User.password == Login.password).first()
    if not db_login:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return{"message":"Login Successfull", "user_id": db_login.user_id}

@app.post("/bank_details creation/",response_model=bankResponse, status_code=status.HTTP_201_CREATED)
def open_account(Bank:bank, db:db_dependency):
    db_bank = bank_models.Bank(**Bank.dict())
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

@app.post("/pin_generation/", response_model=pinResponse, status_code=status.HTTP_201_CREATED)
def pin_generation(pin:pin_generate, db:db_dependency):
    if pin.pin != pin.confirm_pin:
        raise HTTPException(status_code=400, detail="Pin didn't match")
    
    db_bank = db.query(bank_models.Bank).filter(
        bank_models.Bank.account_number == pin.account_number,bank_models.Bank.mobile_number == pin.mobile_number).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Account not found")
    db_bank.pin = pin.pin
    db.commit()
    db.refresh(db_bank)
    return db_bank

@app.post("/Money_deposit/", response_model=depositResponse, status_code=status.HTTP_200_OK)
def deposit(request:depositRequest, db:db_dependency):
    account = db.query(bank_models.Bank).filter(bank_models.Bank.account_number == request.Account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.pin != request.pin:
        raise HTTPException(status_code=401, detail="Incorrct Pin")
    if request.amount <= 0:
        raise HTTPException(status_code=401, detail="Number should be in positive")
    
    account.balance += request.amount
    db.commit()
    db.refresh(account)
    return account

@app.post("/withdraw/", response_model=withdrawResponse, status_code=status.HTTP_200_OK)
def withdraw_money(request: Withdraw_request, db: db_dependency):
    
    account = db.query(bank_models.Bank).filter(
        bank_models.Bank.account_number == request.account_number
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if account.pin != request.pin:
        raise HTTPException(status_code=401, detail="Invalid PIN")

    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Withdraw amount must be positive")

    if account.balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    account.balance -= request.amount
    db.commit()
    db.refresh(account)

    return account

@app.get("/accounts/", status_code=status.HTTP_200_OK)
def get_all_accounts(db: db_dependency):
    accounts = db.query(bank_models.Bank).all()
    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found")
    return accounts

@app.get("/accounts/", status_code=status.HTTP_200_OK)
def get_all_accounts(db: db_dependency):
    accounts = db.query(bank_models.Bank).all()
    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found")
    return accounts

class UpdateAccount(BaseModel):
    mobile_number: str | None = None
    Name: str | None = None
    account_type: str | None = None
    email_id: str | None = None
    Address: str | None = None

@app.put("/accounts/{account_number}", status_code=status.HTTP_200_OK)
def update_account(account_number: int, updated: UpdateAccount, db: db_dependency):
    account = db.query(bank_models.Bank).filter(bank_models.Bank.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(account, key, value)

    db.commit()
    db.refresh(account)
    return {"message": "Account updated successfully", "account_number": account.account_number}

@app.delete("/accounts/{account_number}", status_code=status.HTTP_200_OK)
def delete_account(account_number: int, db: db_dependency):
    account = db.query(bank_models.Bank).filter(bank_models.Bank.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account)
    db.commit()
    return {"message": f"Account {account_number} deleted successfully"}

#Linking Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/banking_system"

engine = create_engine(DATABASE_URL, echo = True)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)

Base = declarative_base()

#Models 
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
