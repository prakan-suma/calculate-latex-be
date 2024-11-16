from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query
from .mongodb import *
from datetime import datetime
from .schemas import PurchaseRecord
from typing import Optional


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/history/")
async def get_history(startDate: Optional[str] = None, endDate: Optional[str] = None, searchTerm: Optional[str] = ''):
    records = await get_purchase_records(startDate, endDate, searchTerm)

    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    return records


@app.post("/history/")
async def create_history(record: PurchaseRecord):
    try:
        new_record_id = await create_purchase_records(record)
        return {"message": "Record created successfully", "id": new_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Delete


@app.delete("/history/{object_id}")
async def delete_history(object_id: str):
    result = await delete_purchase_records(object_id)
    return result
