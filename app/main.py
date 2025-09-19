#import 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.reviews.router import router as reviews_router
from app.bookings.router import router as bookings_router
from app.courses.router import router as courses_router
from app.auth.users.router import router as users_router 
from app.progress_reports.router import router as progress_report_router
from app.class_sessions.router import router as class_session_router
from app.payments.router import router as payment_router
from app.faq_categories.router import router as faq_category_router
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reviews_router, prefix=settings.API_V1_PREFIX)
app.include_router(bookings_router, prefix=settings.API_V1_PREFIX)
app.include_router(users_router, prefix=settings.API_V1_PREFIX)
app.include_router(courses_router, prefix=settings.API_V1_PREFIX)
app.include_router(progress_report_router, prefix=settings.API_V1_PREFIX)
app.include_router(class_session_router, prefix=settings.API_V1_PREFIX)
app.include_router(payment_router, prefix=settings.API_V1_PREFIX)
app.include_router(faq_category_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)