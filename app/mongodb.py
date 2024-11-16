from pymongo import MongoClient
from typing import Optional, List
from bson import ObjectId
from fastapi import HTTPException
from .schemas import PurchaseRecord

# เชื่อมต่อ MongoDB
client = MongoClient(
    "mongodb+srv://prakan:wkkm10456@latexzer-db.mrqji.mongodb.net/?retryWrites=true&w=majority&appName=latexzer-db")
db = client["latexzer_db"]
collection = db["history"]


async def get_purchase_records(startDate: Optional[str], endDate: Optional[str], searchName: Optional[str]) -> List[dict]:
    # Prepare filter dictionary
    filter = {}

    # Filter by date range if startDate and endDate are provided
    if startDate:
        # เรียกใช้ startDate ที่เป็น string ตรง ๆ
        filter["date"] = {"$gte": startDate}

    if endDate:
        # เรียกใช้ endDate ที่เป็น string ตรง ๆ
        if "date" in filter:
            filter["date"]["$lte"] = endDate
        else:
            filter["date"] = {"$lte": endDate}

    # If searchName is provided, filter by seller_name
    if searchName:
        filter["seller_name"] = {"$regex": searchName,
                                 "$options": "i"}  # Case-insensitive search

    # Query MongoDB
    records = list(collection.find(filter))

    # Format the response to match the expected structure
    result = []
    for record in records:
        # คำนวณค่า
        netWeight = record["w_rubber"] - record["w_tank"]
        dryRubber = netWeight * (record["percen"] / 100)
        roundedDryRubber = round(dryRubber * 10) / 10
        totalAmount = round(roundedDryRubber * record["price"])

        result.append({
            "id": str(record["_id"]),
            "date": record["date"],
            "name": record["seller_name"],
            "rubberWeight": record["w_rubber"],
            "tankWeight": record["w_tank"],
            "netWeight": netWeight,
            "percentage": record["percen"],
            "dryRubber": roundedDryRubber,
            "pricePerKg": record["price"],
            "totalAmount": totalAmount
        })

    return result


async def delete_purchase_records(object_id: str):
    if not ObjectId.is_valid(object_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = collection.delete_one({"_id": ObjectId(object_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"message": "Record deleted successfully", "id": object_id}


async def create_purchase_records(record: PurchaseRecord):
    document = record.dict()
    result = collection.insert_one(document)
    return str(result.inserted_id)
