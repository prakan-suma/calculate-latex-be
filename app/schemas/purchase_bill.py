from datetime import datetime
from pydantic import BaseModel


class PurchaseCreate(BaseModel):
    date: str
    name: str
    rubberWeight: float
    tankWeight: float
    netWeight: float
    percentage: float
    dryRubberWeight: float
    buyingPrice: float
    totalAmount: float
    note: str
    noteAmount: float


class PurchaseResponse(BaseModel):
    id: str
    date: str
    name: str
    rubberWeight: float
    tankWeight: float
    netWeight: float
    percentage: float
    dryRubberWeight: float
    buyingPrice: float
    totalAmount: float
    note: str
    noteAmount: float
