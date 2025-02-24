import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.receipts.models import Receipt


@pytest.mark.asyncio(loop_scope="session")
async def test_create_receipt(
    receipt_data, access_token, client: AsyncClient, db_session: AsyncSession
):
    response = await client.post(
        "api/v1/receipts/",
        json=receipt_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"]

    query = select(Receipt).filter_by(amount=receipt_data["payment"]["amount"])
    result = await db_session.execute(query)
    created_receipt = result.scalar_one_or_none()

    assert created_receipt is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_receipt_without_products(
    receipt_data, access_token, client: AsyncClient, db_session: AsyncSession
):
    receipt_data.pop("products")
    response = await client.post(
        "api/v1/receipts/",
        json=receipt_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert response_data["detail"][0]["loc"] == ["body", "products"]
    assert response_data["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_receipt_small_amount(
    receipt_data, access_token, client: AsyncClient, db_session: AsyncSession
):
    receipt_data["payment"]["amount"] = 1.0
    response = await client.post(
        "api/v1/receipts/",
        json=receipt_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert response_data["detail"] == [
        "rest: Input should be greater than or equal to 0"
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_retrieve_receipt(
    receipt, access_token, client: AsyncClient, db_session: AsyncSession
):
    response = await client.get(
        f"api/v1/receipts/{receipt['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == receipt["id"]


@pytest.mark.asyncio(loop_scope="session")
async def test_retrieve_receipt_not_found(
    receipt, access_token, client: AsyncClient, db_session: AsyncSession
):
    response = await client.get(
        f"api/v1/receipts/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Receipt not found"


@pytest.mark.asyncio(loop_scope="session")
async def test_print_receipt(
    receipt, access_token, client: AsyncClient, db_session: AsyncSession
):
    response = await client.get(f"api/v1/receipts/{receipt['id']}/print")
    assert response.status_code == status.HTTP_200_OK
    assert response.text


@pytest.mark.asyncio(loop_scope="session")
async def test_print_receipt_not_found(
    receipt, access_token, client: AsyncClient, db_session: AsyncSession
):
    response = await client.get(f"api/v1/receipts/{uuid.uuid4()}/print")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Receipt not found"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_list_receipts(
    receipt, access_token, client: AsyncClient, db_session: AsyncSession
):
    response = await client.get(
        f"api/v1/receipts/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["total"] == len(response_data["items"]) == 1
    assert response_data["pages"] == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_list_receipts_with_pagination(
    receipt_data, access_token, client: AsyncClient, db_session: AsyncSession
):
    headers = {"Authorization": f"Bearer {access_token}"}

    # First receipt
    response = await client.post("api/v1/receipts/", json=receipt_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    # Second receipt
    receipt_data["payment"]["type"] = "CASHLESS"
    response = await client.post("api/v1/receipts/", json=receipt_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    # Third receipt
    test_product = {"name": "Test product", "price": 1488.00, "quantity": 5}
    receipt_data["products"].append(test_product)
    receipt_data["payment"]["amount"] += (
        test_product["price"] * test_product["quantity"]
    )
    response = await client.post("api/v1/receipts/", json=receipt_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get(f"api/v1/receipts/?size=2&page=1", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["total"] == 3
    assert len(response_data["items"]) == 2
    assert response_data["pages"] == 2


@pytest.mark.asyncio(loop_scope="session")
async def test_get_list_receipts_with_filters(
    receipt_data, access_token, client: AsyncClient, db_session: AsyncSession
):
    headers = {"Authorization": f"Bearer {access_token}"}

    # First receipt
    cashless_receipt1_response = await client.post(
        "api/v1/receipts/", json=receipt_data, headers=headers
    )
    assert cashless_receipt1_response.status_code == status.HTTP_201_CREATED
    cashless_receipt1 = cashless_receipt1_response.json()

    # Second receipt
    receipt_data["payment"]["type"] = "CASH"
    cash_receipt_response = await client.post(
        "api/v1/receipts/", json=receipt_data, headers=headers
    )
    assert cash_receipt_response.status_code == status.HTTP_201_CREATED
    cash_receipt = cash_receipt_response.json()

    # Third receipt
    test_product = {"name": "Test product", "price": 1488.00, "quantity": 5}
    receipt_data["payment"]["type"] = "CASHLESS"
    receipt_data["products"].append(test_product)
    receipt_data["payment"]["amount"] += (
        test_product["price"] * test_product["quantity"]
    )
    cashless_receipt2_response = await client.post(
        "api/v1/receipts/", json=receipt_data, headers=headers
    )
    assert cashless_receipt2_response.status_code == status.HTTP_201_CREATED
    cashless_receipt2 = cashless_receipt2_response.json()

    response = await client.get(
        f"api/v1/receipts/?payment_types=CASHLESS&size=20&page=1", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["total"] == 2 == len(response_data["items"])
    assert response_data["pages"] == 1
    assert response_data["size"] == 20

    response_items_ids = [item["id"] for item in response_data["items"]]
    assert cash_receipt["id"] not in response_items_ids
    assert cashless_receipt1["id"] in response_items_ids
    assert cashless_receipt2["id"] in response_items_ids
