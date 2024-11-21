from datetime import datetime
from app.core.database import db
from app.schemas.sales_bill import SalesCreate, SalesResponse
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

sales_collection = db["sales_bills"]

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


async def create_sales(sales: SalesCreate):
    try:
        sales_date = sales.date
        sales_doc = {
            "totalDryRubberWeight": round(sales.totalDryRubberWeight, 1),
            "pricePurchase": round(sales.pricePurchase, 1),
            "serviceCharge": round(sales.serviceCharge, 1),
            "totalAmount": round(sales.totalAmount, 1),
            "date": str(sales_date)
        }

        result = await sales_collection.insert_one(sales_doc)

        return str(result.inserted_id)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while saving sales: {str(e)}")


async def get_sales_by_date(start_date: str, end_date: str):
    try:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")

        sales = await sales_collection.find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).to_list(length=None)

        if not sales:
            raise HTTPException(
                status_code=404, detail="No sales bill found in this date range."
            )

        return [
            SalesResponse(
                id=str(sale["_id"]),
                totalDryRubberWeight=sale["totalDryRubberWeight"],
                pricePurchase=sale["pricePurchase"],
                serviceCharge=sale["serviceCharge"],
                totalAmount=sale["totalAmount"],
                date=sale["date"]
            ) for sale in sales
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while retrieving sales: {str(e)}"
        )


async def get_total_amount_by_month(start_date: str, end_date: str):
    try:

        sales = await sales_collection.find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).to_list(length=None)

        if not sales:
            raise HTTPException(
                status_code=404, detail="No sales found in this date range."
            )

        monthly_totals = {}

        for sales in sales:

            sales_date = datetime.strptime(sales["date"], "%Y-%m-%d")
            month_name = sales_date.strftime("%B")

            thai_month_name = MONTHS_IN_THAI.get(month_name, month_name)

            if thai_month_name not in monthly_totals:
                monthly_totals[thai_month_name] = 0

            monthly_totals[thai_month_name] += sales["totalAmount"]

        result = [{"month": month, "totalAmount": round(
            amount, 0)} for month, amount in monthly_totals.items()]

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while calculating total amounts by month: {str(e)}"
        )


async def update_sales(sales_id: str, sales: SalesCreate):
    try:
        sales_object_id = ObjectId(sales_id)

        update_doc = {
            "totalDryRubberWeight": round(sales.totalDryRubberWeight, 1),
            "pricePurchase": round(sales.pricePurchase, 1),
            "serviceCharge": round(sales.serviceCharge, 1),
            "totalAmount": round(sales.totalAmount, 1),
            "date": sales.date
        }

        result = await sales_collection.update_one(
            {"_id": sales_object_id}, {"$set": update_doc}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404, detail="Sale not found."
            )

        return {"message": "Sale updated successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while updating sales: {str(e)}"
        )


async def delete_sales(sales_id: str):
    try:
        sales_object_id = ObjectId(sales_id)

        result = await sales_collection.delete_one({"_id": sales_object_id})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="Sale not found."
            )

        return {"message": "Sale deleted successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while deleting sales: {str(e)}"
        )
