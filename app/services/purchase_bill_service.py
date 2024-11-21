from datetime import datetime
from app.core.database import db
from app.schemas.purchase_bill import PurchaseCreate, PurchaseResponse
from fastapi import HTTPException
from bson import ObjectId

purchase_collection = db["purchase_bills"]

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


async def create_purchase(purchase: PurchaseCreate):
    try:
        purchase_date = purchase.date

        purchase_doc = {
            "name": purchase.name,
            "rubberWeight": purchase.rubberWeight,
            "tankWeight": purchase.tankWeight,
            "netWeight": purchase.netWeight,
            "percentage": purchase.percentage,
            "dryRubberWeight": purchase.dryRubberWeight,
            "buyingPrice": purchase.buyingPrice,
            "totalAmount": purchase.totalAmount,
            "date": purchase_date,
            "note": purchase.note,
            "noteAmount": purchase.noteAmount
        }

        result = await purchase_collection.insert_one(purchase_doc)
        return str(result.inserted_id)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while saving purchase: {str(e)}"
        )


async def get_total_dry_rubber_weight_by_date(start_date: str, end_date: str):
    try:
        purchases = await purchase_collection.find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).to_list(length=None)

        if not purchases:
            raise HTTPException(
                status_code=404, detail="No purchases found in this date range."
            )

        total_dry_rubber_weight = sum(
            purchase["dryRubberWeight"] for purchase in purchases)

        return {"total_dry_rubber_weight": round(total_dry_rubber_weight, 1)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while calculating total dry rubber weight: {str(e)}"
        )


async def get_total_amount_by_month(start_date: str, end_date: str):
    try:

        purchases = await purchase_collection.find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).to_list(length=None)

        if not purchases:
            raise HTTPException(
                status_code=404, detail="No purchases found in this date range."
            )

        monthly_totals = {}

        for purchase in purchases:

            purchase_date = datetime.strptime(purchase["date"], "%Y-%m-%d")
            month_name = purchase_date.strftime("%B")

            thai_month_name = MONTHS_IN_THAI.get(month_name, month_name)

            if thai_month_name not in monthly_totals:
                monthly_totals[thai_month_name] = 0

            monthly_totals[thai_month_name] += purchase["totalAmount"]

        result = [{"month": month, "totalAmount": round(
            amount, 0)} for month, amount in monthly_totals.items()]

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while calculating total amounts by month: {str(e)}"
        )


async def get_purchases_by_date(start_date: str, end_date: str):
    try:

        purchases = await purchase_collection.find({
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).to_list(length=None)

        if not purchases:
            raise HTTPException(
                status_code=404, detail="No purchases found in this date range."
            )

        return [
            PurchaseResponse(
                id=str(purchase["_id"]),
                name=purchase["name"],
                rubberWeight=purchase["rubberWeight"],
                tankWeight=purchase["tankWeight"],
                netWeight=purchase["netWeight"],
                percentage=purchase["percentage"],
                dryRubberWeight=purchase["dryRubberWeight"],
                buyingPrice=purchase["buyingPrice"],
                totalAmount=purchase["totalAmount"],
                date=purchase["date"],
                note=purchase["note"],
                noteAmount=purchase["noteAmount"]
            ) for purchase in purchases
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while retrieving purchases: {str(e)}"
        )


async def update_purchase(purchase_id: str, purchase: PurchaseCreate):
    try:
        purchase_object_id = ObjectId(purchase_id)

        update_doc = {
            "name": purchase.name,
            "rubberWeight": purchase.rubberWeight,
            "tankWeight": purchase.tankWeight,
            "netWeight": purchase.netWeight,
            "percentage": purchase.percentage,
            "dryRubberWeight": purchase.dryRubberWeight,
            "buyingPrice": purchase.buyingPrice,
            "totalAmount": purchase.totalAmount,
            "date": purchase.date,
            "note": purchase.note,
            "noteAmount": purchase.noteAmount
        }

        result = await purchase_collection.update_one(
            {"_id": purchase_object_id}, {"$set": update_doc}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404, detail="Purchase not found."
            )

        return {"message": "Purchase updated successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while updating purchase: {str(e)}"
        )


async def delete_purchase(purchase_id: str):
    try:
        purchase_object_id = ObjectId(purchase_id)

        result = await purchase_collection.delete_one({"_id": purchase_object_id})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="Purchase not found."
            )

        return {"message": "Purchase deleted successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while deleting purchase: {str(e)}"
        )
