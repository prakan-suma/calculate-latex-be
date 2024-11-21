from datetime import datetime
from app.core.database import db
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId

expense_collection = db["expense_list"]

MONTHS_IN_THAI = {
    "January": "มกราคม",
    "February": "กุมภาพันธ์",
    "March": "มีนาคม",
    "April": "เมษายน",
    "May": "พฤษภาคม",
    "June": "มิถุนายน",
    "July": "กรกฎาคม",
    "August": "สิงหาคม",
    "September": "กันยายน",
    "October": "ตุลาคม",
    "November": "พฤศจิกายน",
    "December": "ธันวาคม"
}


async def create_expense(expense: ExpenseCreate):
    try:
        expense_date = expense.date

        expense_doc = {
            "note": expense.note,
            "amount": round(expense.amount, 1),
            "date": str(expense_date)
        }

        result = await expense_collection.insert_one(expense_doc)

        return str(result.inserted_id)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while saving expense: {str(e)}")


async def get_expense_by_date(start_date: str, end_date: str):
    try:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")

        expenses = await expense_collection.find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).to_list(length=None)

        if not expenses:
            raise HTTPException(
                status_code=404, detail="No expense bill found in this date range."
            )

        return [
            ExpenseResponse(
                id=str(expense["_id"]),
                note=expense["note"],
                amount=expense["amount"],
                date=expense["date"]
            ) for expense in expenses
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while retrieving expense: {str(e)}"
        )


async def get_total_amount_by_month(start_date: str, end_date: str):
    try:
        # ค้นหาข้อมูลทั้งหมดภายในช่วงเวลา
        expense = await expense_collection.find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).to_list(length=None)

        if not expense:
            raise HTTPException(
                status_code=404, detail="No expense found in this date range."
            )

        # ใช้ dictionary สำหรับการรวมยอดตามเดือน
        monthly_totals = {}

        # ประมวลผลข้อมูลการซื้อทั้งหมด
        for expense in expense:
            # แปลงวันที่จาก string เป็น datetime object
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            month_name = expense_date.strftime("%B")  # ชื่อเดือนภาษาอังกฤษ

            # แปลงชื่อเดือนจากภาษาอังกฤษเป็นภาษาไทย
            thai_month_name = MONTHS_IN_THAI.get(month_name, month_name)

            # หากเดือนนี้ยังไม่มีใน dictionary, ให้เพิ่มเดือนใหม่
            if thai_month_name not in monthly_totals:
                monthly_totals[thai_month_name] = 0

            # รวมยอดตามเดือน
            monthly_totals[thai_month_name] += expense["amount"]

        # สร้างผลลัพธ์ที่ต้องการในรูปแบบที่มีชื่อเดือนและยอดรวม
        result = [{"month": month, "totalAmount": round(
            amount, 0)} for month, amount in monthly_totals.items()]

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while calculating total amounts by month: {str(e)}"
        )


async def update_expense(expense_id: str, expense: ExpenseCreate):
    try:
        expense_object_id = ObjectId(expense_id)

        update_doc = {
            "note": expense.note,
            "amount": expense.amount,
            "date": expense.date
        }

        result = await expense_collection.update_one(
            {"_id": expense_object_id}, {"$set": update_doc}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404, detail="Expense not found."
            )

        return {"message": "Expense updated successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while updating expense: {str(e)}"
        )


async def delete_expense(expense_id: str):
    try:
        expense_object_id = ObjectId(expense_id)

        result = await expense_collection.delete_one({"_id": expense_object_id})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="Expense not found."
            )

        return {"message": "Expense deleted successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while deleting expense: {str(e)}"
        )
