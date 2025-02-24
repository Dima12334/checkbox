import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.users.models import User


@pytest.mark.asyncio(loop_scope="session")
async def test_sign_up(user_data, client: AsyncClient, db_session: AsyncSession):
    response = await client.post("api/v1/auth/sign-up", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["company_name"] == user_data["company_name"]
    assert response.json()["email"] == user_data["email"]

    query = select(User).filter_by(email=user_data["email"])
    result = await db_session.execute(query)
    created_user = result.scalar_one_or_none()

    assert created_user is not None
    assert created_user.email == user_data["email"]
    assert created_user.company_name == user_data["company_name"]


@pytest.mark.asyncio(loop_scope="session")
async def test_sign_up_user_already_exists(
    user, user_data, client: AsyncClient, db_session: AsyncSession
):
    response = await client.post("api/v1/auth/sign-up", json=user_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Object already exists."


@pytest.mark.asyncio(loop_scope="session")
async def test_sign_in(user, client: AsyncClient):
    response = await client.post(
        "api/v1/auth/sign-in",
        json={"email": user["email"], "password": user["password"]},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio(loop_scope="session")
async def test_sign_in_wrong_email(user, client: AsyncClient):
    email = "a" + user["email"]
    response = await client.post(
        "api/v1/auth/sign-in",
        json={"email": email, "password": user["password"]},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."


@pytest.mark.asyncio(loop_scope="session")
async def test_sign_in_wrong_password(user, client: AsyncClient):
    password = "a" + user["password"]
    response = await client.post(
        "api/v1/auth/sign-in",
        json={"email": user["email"], "password": password},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."
