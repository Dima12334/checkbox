import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.users.models import User


@pytest.mark.asyncio(loop_scope="session")
async def test_sign_up(user, client: AsyncClient, db_session: AsyncSession):
    user["email"] = "test@test.com"
    response = await client.post("api/v1/auth/sign-up", json=user)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["company_name"] == user["company_name"]
    assert response.json()["email"] == "test@test.com"

    query = select(User).filter_by(email=user["email"])
    result = await db_session.execute(query)
    created_user = result.scalar_one_or_none()

    assert created_user is not None
    assert created_user.email == "test@test.com"
    assert created_user.company_name == user["company_name"]


@pytest.mark.asyncio(loop_scope="session")
async def test_sign_in(user, client: AsyncClient):
    response = await client.post(
        "api/v1/auth/sign-in",
        json={"email": user["email"], "password": user["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"
