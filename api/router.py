from fastapi import APIRouter
from features.headlines.routes import router as headlines_router

api_router = APIRouter()
api_router.include_router(headlines_router)
