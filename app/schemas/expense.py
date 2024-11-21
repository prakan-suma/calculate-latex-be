from datetime import datetime
from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    date: str
    note: str
    amount: float


class ExpenseResponse(BaseModel):
    id: str
    date: str
    note: str
    amount: float
