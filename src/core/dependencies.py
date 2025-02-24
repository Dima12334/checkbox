from datetime import datetime, timezone
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_async_session
from src.core.exceptions import InvalidTokenException, ExpiredTokenException
from src.core.schemas.auth_schemas import JWTTokenPayloadSchema
from src.core.services.user_service import UserService
from src.core.utils.jwt import decode_jwt
from src.users.models import User


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    try:
        payload = await decode_jwt(token.credentials)
    except JWTError:
        raise InvalidTokenException()

    payload = JWTTokenPayloadSchema(**payload)
    if payload.exp.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        raise ExpiredTokenException()

    user_service = UserService()
    current_user = await user_service.get_by_id(object_id=payload.id, db=db)
    return current_user
