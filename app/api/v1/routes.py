from fastapi import APIRouter
from .endpoints import purchase_bill, sales_bill, expense

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


router.include_router(purchase_bill.router, tags=["Purchase Bill"])
router.include_router(sales_bill.router, tags=["Sales Bill"])
router.include_router(expense.router, tags=["Expense"])
