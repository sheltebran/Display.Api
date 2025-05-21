# FastAPI app instantiation and startup

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.router import api_router
from core.database import create_database_if_not_exists, create_headline_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_if_not_exists()
    create_headline_table()
    yield

app = FastAPI(
    title="Display.API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Service running"}
