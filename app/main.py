from contextlib import asynccontextmanager
from pathlib import Path
import logging
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base, engine, get_db
from . import crud
from .schemas import UserCreate, UserUpdate, UserResponse, UserLogin
from .auth import create_access_token, get_current_user, check_user_access

from .logger import setup_logging
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


@app.post("/login")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    user = await crud.authenticate_user(
        db,
        user_data.email,
        user_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post("/users",response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    logger.info(
        "Creating new user",
        extra={
            "event": "user_creation_started",
            "operation": "create_user"
        }
    )
    return await crud.create_user(db, user)

@app.get("/users")
async def get_users(
    search: str | None = Query(
        default=None,
        description="Search users by name or email"
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number"
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of users per page"
    ),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await crud.get_users(
        db,
        search,
        page,
        page_size
    )

@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
async def get_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    user = await crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.put("/users/{user_id}",response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(check_user_access)
):
    current_user_id = getattr(current_user, "id", current_user)

    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this user"
        )

    user = await crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return await crud.update_user(
        db,
        user,
        user_data
    )

@app.delete("/users/{user_id}",response_model=UserResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(check_user_access)
):
    current_user_id = getattr(current_user, "id", current_user)

    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this user"
        )

    user = await crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    await crud.delete_user(db, user)

    return {
        "message": "User deleted successfully"
    }

SOURCE_FILE = Path("logs/app.log")
OUTPUT_FILE = Path("downloads/app-log-copy.log")

@app.post("/download_logs")
async def generate_file():

    try:

        with open(SOURCE_FILE,'r') as file:
            data = file.read()


        OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(OUTPUT_FILE, "w") as file:
            file.write(data)


        return FileResponse(
            OUTPUT_FILE,
            filename="app-log-copy.log"
        )

    except HTTPException:
        raise