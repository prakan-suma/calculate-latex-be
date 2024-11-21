from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_db_url: str
    mongo_db_name: str

    class Config:
        env_file = ".env"


# สร้าง instance ของ Settings
settings = Settings()
