import os
from dotenv import load_dotenv
load_dotenv()



import jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
ALGORITHM = os.getenv("ALGORITHM")

PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH")


with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()


security = HTTPBearer()

def create_access_token(user_id: int):

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=30),
        "iss": "fastapi-auth",
        "aud": "user-api"
    }

    token = jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm=ALGORITHM
    )
    return token

def verify_access_token(token: str):

    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM],
            audience="user-api",
            issuer="fastapi-auth"
        )
        return payload

    except jwt.ExpiredSignatureError:
        print("JWT ERROR: TOKEN EXPIRED")

        return None

    except jwt.InvalidIssuerError:
        print("JWT ERROR: INVALID ISSUER")
        return None

    except jwt.InvalidTokenError as e:
        print("JWT ERROR:", e)

        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return int(user_id)



async def check_user_access(
    user_id: int,
    current_user: int = Depends(get_current_user)
):

    if current_user != user_id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this user"
        )

    return current_user