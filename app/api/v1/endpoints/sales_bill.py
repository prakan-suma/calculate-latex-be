from fastapi import APIRouter, HTTPException, status
from app.schemas.sales_bill import SalesCreate, SalesResponse
from app.services.sales_bill_service import create_sales, get_sales_by_date, delete_sales, update_sales, get_total_amount_by_month
from typing import List

router = APIRouter()


@router.post("/sales", response_model=str)
async def create_new_sales(sales: SalesCreate):
    sales_id = await create_sales(sales)
    if not sales_id:
        raise HTTPException(status_code=500, detail="Cannot create sales")
    return sales_id


@router.get("/sales", response_model=List[SalesResponse])
async def get_sales(start_date: str, end_date: str):
    try:
        sales = await get_sales_by_date(start_date, end_date)
        return sales
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/sales/total-amount")
async def get_total_amount(start_date: str, end_date: str):
    try:
        total_amount = await get_total_amount_by_month(start_date, end_date)
        return total_amount
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/sales/{sales_id}", response_model=dict)
async def update_sales_info(sales_id: str, sales: SalesCreate):
    try:
        await update_sales(sales_id, sales)
        return {"message": "Sales updated successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# DELETE /sales/{sales_id} สำหรับลบข้อมูล sales
@router.delete("/sales/{sales_id}", response_model=dict)
async def delete_sales_info(sales_id: str):
    try:
        await delete_sales(sales_id)
        return {"message": "Sales deleted successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
