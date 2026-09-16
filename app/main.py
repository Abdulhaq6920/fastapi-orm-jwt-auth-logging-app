from contextlib import asynccontextmanager
import logging
from fastapi import Depends, FastAPI
from app.routes import auth, users, logs
from .database import Base, engine

from app.logger import setup_logging
setup_logging()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):


    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Application started successfully")
    yield

    await engine.dispose()
    logger.info("Application shut down successfully")

app = FastAPI(
    title="FastAPI User Management App with JWT Authentication",
    description="A FastAPI application.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(logs.router)

