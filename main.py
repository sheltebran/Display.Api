# FastAPI app instantiation and startup
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.router import api_router
from core.database import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
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
