from pydantic import BaseModel


class SalesCreate(BaseModel):
    date: str
    totalDryRubberWeight: float
    pricePurchase: float
    serviceCharge: float
    totalAmount: float


class SalesResponse(BaseModel):
    id: str
    date: str
    totalDryRubberWeight: float
    pricePurchase: float
    serviceCharge: float
    totalAmount: float
