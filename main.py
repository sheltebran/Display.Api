# FastAPI app instantiation and startup
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.router import api_router
from core.database import initialize_database
from events.rabbitmq_handler import rabbitmq_listener
from features.headlines.routes import router as list_headlines

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await initialize_database()
    # Save the task to prevent premature garbage collection
    _app.state.rabbitmq_task = asyncio.create_task(rabbitmq_listener())
    yield

app = FastAPI(
    title="Display.API",
    version="1.0.0",
    redirect_slashes=False,
    lifespan=lifespan
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Service running"}

    