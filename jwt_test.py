import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "my-super-secret-key-that-is-at-least-32-bytes-long"
ALGORITHM = "HS256"

now = datetime.now(timezone.utc)

payload = {
    "sub": "133",
    "iss": "fastapi-auth",
    "iat": now,
    "exp": now + timedelta(seconds=30),
}

token = jwt.encode(
    payload,
    SECRET_KEY,
    algorithm=ALGORITHM
)

print("Generated JWT token:")
print(token)

decoded = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)

print("\nDecoded JWT:")
print(decoded)