import pytest_asyncio


@pytest_asyncio.fixture(loop_scope="session")
async def user(client):
    user = {
        "first_name": "first_name",
        "last_name": "last_name",
        "company_name": "FOP company_name",
        "email": "email@test.com",
        "password": "password",
    }
    response = await client.post("/api/v1/auth/sign-up", json=user)
    data = response.json()
    user["id"] = data["id"]

    return user


@pytest_asyncio.fixture(loop_scope="session")
async def access_token(client, user):
    await client.post("/api/v1/auth/sign-up", json=user)
    response = await client.post(
        "/api/v1/auth/sign-in",
        json={"email": user["email"], "password": user["password"]},
    )
    data = response.json()
    return data["access_token"]
