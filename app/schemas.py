from pydantic import BaseModel
from typing import List


class PurchaseRecord(BaseModel):
    seller_name: str
    w_rubber: float
    w_tank: float
    percen: float
    price: float
    date: str


class PurchaseRecords(BaseModel):
    records: List[PurchaseRecord]
