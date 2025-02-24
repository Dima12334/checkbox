import uuid
from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import settings
from src.core.schemas.auth_schemas import JWTTokenPayloadSchema
from src.core.utils.jwt import encode_jwt


@pytest.mark.asyncio(loop_scope="session")
async def test_me(user, access_token, client: AsyncClient, db_session: AsyncSession):
    response = await client.get(
        "api/v1/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == user["email"]


@pytest.mark.asyncio(loop_scope="session")
async def test_me_token_expired(user, client: AsyncClient):
    payload = JWTTokenPayloadSchema(id=user["id"], exp=datetime.utcnow())
    access_token = await encode_jwt(payload.dict())

    response = await client.get(
        "api/v1/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token has expired."


@pytest.mark.asyncio(loop_scope="session")
async def test_me_wrong_token(user, client: AsyncClient):
    payload = JWTTokenPayloadSchema(
        id=str(uuid.uuid4()),
        exp=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    access_token = await encode_jwt(payload.dict())

    response = await client.get(
        "api/v1/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token."
