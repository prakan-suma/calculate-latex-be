from fastapi import APIRouter, HTTPException, status
from app.schemas.purchase_bill import PurchaseCreate, PurchaseResponse
from app.services.purchase_bill_service import create_purchase, get_purchases_by_date, get_total_dry_rubber_weight_by_date, update_purchase, delete_purchase, get_total_amount_by_month
from typing import List

router = APIRouter()

# POST /purchase สำหรับสร้างข้อมูล purchase ใหม่


@router.post("/purchase", response_model=str)
async def create_new_purchase(purchase: PurchaseCreate):
    purchase_id = await create_purchase(purchase)
    if not purchase_id:
        raise HTTPException(status_code=500, detail="Cannot create purchase")
    return purchase_id


# GET /purchases สำหรับดึงข้อมูล purchase ตามช่วงเวลา
@router.get("/purchases", response_model=List[PurchaseResponse])
async def get_purchases(start_date: str, end_date: str):
    try:
        purchases = await get_purchases_by_date(start_date, end_date)
        return purchases
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# GET /total-dry-rubber สำหรับดึงน้ำหนักยางแห้งรวมตามช่วงเวลา
@router.get("/total-dry-rubber")
async def get_dry_rubber(start_date: str, end_date: str):
    try:
        purchases = await get_total_dry_rubber_weight_by_date(start_date, end_date)
        return purchases
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/purchases/total-amount")
async def get_total_amount(start_date: str, end_date: str):
    try:
        total_amount = await get_total_amount_by_month(start_date, end_date)
        return total_amount
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/purchase/{purchase_id}", response_model=dict)
async def update_purchase_info(purchase_id: str, purchase: PurchaseCreate):
    try:
        await update_purchase(purchase_id, purchase)
        return {"message": "Purchase updated successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# DELETE /purchase/{purchase_id} สำหรับลบข้อมูล purchase
@router.delete("/purchase/{purchase_id}", response_model=dict)
async def delete_purchase_info(purchase_id: str):
    try:
        await delete_purchase(purchase_id)
        return {"message": "Purchase deleted successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
