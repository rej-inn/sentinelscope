import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "SentinelScope"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sentinelscope.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
