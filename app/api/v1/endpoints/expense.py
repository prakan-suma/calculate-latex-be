from fastapi import APIRouter, HTTPException, status
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.expense_service import create_expense, get_expense_by_date, update_expense, delete_expense, get_total_amount_by_month

from typing import List

router = APIRouter()


@router.post("/expense", response_model=str)
async def create_new_expense(purchase: ExpenseCreate):
    expense_id = await create_expense(purchase)
    if not expense_id:
        raise HTTPException(status_code=500, detail="Cannot create expense")
    return expense_id


@router.get("/expense", response_model=List[ExpenseResponse])
async def get_expense(start_date: str, end_date: str):
    try:
        expense = await get_expense_by_date(start_date, end_date)
        return expense
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/expense/total-amount")
async def get_total_amount(start_date: str, end_date: str):
    try:
        total_amount = await get_total_amount_by_month(start_date, end_date)
        return total_amount
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/expense/{expense_id}", response_model=dict)
async def update_expense_info(expense_id: str, expense: ExpenseCreate):
    try:
        await update_expense(expense_id, expense)
        return {"message": "Expense updated successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# DELETE /expense/{expense_id} สำหรับลบข้อมูล expense
@router.delete("/expense/{expense_id}", response_model=dict)
async def delete_expense_info(expense_id: str):
    try:
        await delete_expense(expense_id)
        return {"message": "Expense deleted successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
