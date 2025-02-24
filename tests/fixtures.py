import pytest_asyncio
from starlette import status


@pytest_asyncio.fixture(loop_scope="session")
async def user_data(client):
    user_data = {
        "first_name": "first_name",
        "last_name": "last_name",
        "company_name": "FOP company_name",
        "email": "email@test.com",
        "password": "password",
    }
    return user_data


@pytest_asyncio.fixture(loop_scope="session")
async def user(user_data, client):
    response = await client.post("/api/v1/auth/sign-up", json=user_data)
    data = response.json()
    user_data["id"] = data["id"]

    return user_data


@pytest_asyncio.fixture(loop_scope="session")
async def access_token(client, user):
    response = await client.post(
        "/api/v1/auth/sign-in",
        json={"email": user["email"], "password": user["password"]},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    return data["access_token"]


@pytest_asyncio.fixture(loop_scope="session")
async def receipt_data(client):
    receipt_data = {
        "products": [
            {"name": "Mavic 3T", "price": 298870.00, "quantity": 3},
            {
                "name": "Дрон FPV з акумулятором 6S чорний",
                "price": 31000.00,
                "quantity": 20,
            },
        ],
        "payment": {"type": "CASHLESS", "amount": 1516610.00},
    }
    return receipt_data


@pytest_asyncio.fixture(loop_scope="session")
async def receipt(receipt_data, access_token, client):
    response = await client.post(
        "/api/v1/receipts/",
        json=receipt_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    return data
