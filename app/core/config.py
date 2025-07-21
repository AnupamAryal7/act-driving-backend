from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    PROJECT_NAME: str = "ACT Backend API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A comprehensive backend API for ACT-Capital-Driving-School"
    API_V1_PREFIX: str = "/api/v1"

settings = Settings()