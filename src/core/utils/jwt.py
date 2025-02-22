from datetime import datetime, timedelta
from typing import Dict, Any
from jose import jwt
from config import settings
from src.core.schemas.auth_schemas import JWTTokenPayloadSchema
from src.users.models import User


async def encode_jwt(payload: Dict[str, Any]) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def decode_jwt(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


async def create_jwt(user: User, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = JWTTokenPayloadSchema(id=str(user.id), exp=expire)
    access_token = await encode_jwt(payload.dict())

    return access_token
