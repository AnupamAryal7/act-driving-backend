from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    PROJECT_NAME: str = "ACT Backend API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A comprehensive backend API for ACT-Capital-Driving-School"
    API_V1_PREFIX: str = "/api/v1"

    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")

settings = Settings()