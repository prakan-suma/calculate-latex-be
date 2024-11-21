from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# สร้างการเชื่อมต่อกับ MongoDB Atlas
client = AsyncIOMotorClient(settings.mongo_db_url)
db = client[settings.mongo_db_name]


# ตรวจสอบการเชื่อมต่อ (Optional)
try:
    client.admin.command('ping')
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print("Failed to connect to MongoDB Atlas:", e)
