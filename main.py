# FastAPI app instantiation and startup
import asyncio
import logging
import seqlog
import yaml
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

# Configure logging to send to Seq
# log_to_seq(
#     server_url="http://localhost:5341",  # Replace with your Seq server URL
#     api_key=None,  # Optional: provide an API key if your Seq server requires it
#     level=logging.INFO,  # Set the minimum logging level
#     batch_interval=1,  # How often to send logs (in seconds)
# )
# with open('core/logging_config.yaml', 'r') as f:
#     config = yaml.safe_load(f)
#     seqlog.configure_from_dict(config) # Use configure_from_dict() for dictionary configuration
seqlog.configure_from_file('core/logging_config.yml')

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
