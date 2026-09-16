from fastapi import HTTPException, Depends, APIRouter
from app.auth import create_access_token
from app.database import get_db, AsyncSession
from app.schemas import UserLogin
from app.crud import authenticate_user
import dotenv
dotenv.load_dotenv()
router = APIRouter(prefix=("/auth"),tags=["authentication"])
@router.post("/login")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(
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