from fastapi import HTTPException, Depends, APIRouter, Query
from app.schemas import UserResponse, UserCreate, UserUpdate
from app.database import AsyncSession, get_db
from app.auth import get_current_user, check_user_access
from app.logger import logging
from app import crud
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users",tags=["User"])

@router.post("/users",response_model=UserResponse)
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


@router.get("/users")
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
@router.get("/users/{user_id}",response_model=UserResponse)
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

@router.put("/users/{user_id}",response_model=UserResponse)
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


@router.delete("/users/{user_id}",response_model=UserResponse)
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