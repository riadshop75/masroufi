from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.core.config import settings
from app.routes import auth
import os

# Import models to ensure they're registered with SQLAlchemy
from app.models import User, Category, Expense, RecurringExpense, Budget, ApiToken

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Application de suivi des dépenses personnelles"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
from app.routes import expenses, categories, budgets, recurring, dashboard, export, api_tokens
app.include_router(expenses.router)
app.include_router(categories.router)
app.include_router(budgets.router)
app.include_router(recurring.router)
app.include_router(dashboard.router)
app.include_router(export.router)
app.include_router(api_tokens.router)

# Start recurring expenses scheduler
from app.tasks.recurring_worker import start_scheduler
scheduler = start_scheduler()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/v1/health")
async def api_health_check():
    return {"status": "ok", "version": settings.API_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
