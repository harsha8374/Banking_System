from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    pin: str
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")
    reason: Optional[str] = None


class TransferResponse(BaseModel):
    transaction_id: int
    from_account: int
    to_account: int
    amount: float
    reason: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
