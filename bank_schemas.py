from pydantic import BaseModel

class Bank(BaseModel):
    account_number: int
    mobile_number: str
    Name: str
    account_type: str
    email_id: str
    Address: str

    class Config:
        orm_mode = True


class BankResponse(Bank):
    bank_id: int


class PinGenerate(BaseModel):
    account_number: int
    mobile_number: str
    pin: str
    confirm_pin: str


class PinResponse(BaseModel):
    bank_id: int


class DepositRequest(BaseModel):
    Account_number: int
    amount: float
    pin: str


class DepositResponse(BaseModel):
    account_number: int
    balance: float

    class Config:
        orm_mode = True


class WithdrawRequest(BaseModel):
    account_number: int
    pin: str
    amount: int


class WithdrawResponse(BaseModel):
    account_number: int
    pin: str
    balance: float

    class Config:
        orm_mode = True


class UpdateAccount(BaseModel):
    mobile_number: str | None = None
    Name: str | None = None
    account_type: str | None = None
    email_id: str | None = None
    Address: str | None = None
