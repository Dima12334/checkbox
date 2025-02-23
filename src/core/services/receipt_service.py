from typing import List
from uuid import UUID

from fastapi_pagination import Params, Page
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from src.core.filters.receipt_filters import ReceiptFilter
from src.core.repositories.receipt_product_repository import ReceiptProductRepository
from src.core.repositories.receipt_repository import ReceiptRepository
from src.core.schemas.receipt_schemas import (
    ReceiptCreateInSchema,
    ReceiptCreateOutSchema,
    ReceiptProductReadSchema,
    ReceiptProductCreateOutSchema,
    ReceiptReadSchema,
    PaymentSchema,
)
from src.core.services.base_service import BaseService
from src.receipts.models import Receipt
from src.users.models import User


class ReceiptService(BaseService):
    repo = ReceiptRepository()
    receipt_product_repo = ReceiptProductRepository()

    async def create(
        self, receipt_info: ReceiptCreateInSchema, user: User, db: AsyncSession
    ) -> ReceiptReadSchema:
        products = [
            ReceiptProductReadSchema(
                name=product.name,
                price=product.price,
                quantity=product.quantity,
                total=product.price * product.quantity,
            )
            for product in receipt_info.products
        ]
        total = sum([product.total for product in products])
        rest = receipt_info.payment.amount - total
        receipt = ReceiptCreateOutSchema(
            user_id=user.id,
            payment_type=receipt_info.payment.type,
            amount=receipt_info.payment.amount,
            rest=rest,
            total=total,
        )
        receipt = await self.repo.create(schema=receipt, db=db)

        receipt_products = [
            ReceiptProductCreateOutSchema(
                receipt_id=receipt.id,
                name=product.name,
                price=product.price,
                quantity=product.quantity,
                total=product.price * product.quantity,
            )
            for product in receipt_info.products
        ]
        await self.receipt_product_repo.create_bulk(schemas=receipt_products, db=db)

        receipt_schema = ReceiptReadSchema(
            id=receipt.id,
            products=products,
            payment=receipt_info.payment,
            total=total,
            rest=rest,
            created_at=receipt.created_at,
        )
        return receipt_schema

    async def get_receipt_by_id_and_user_id(
        self, object_id: UUID | str, user: User, db: AsyncSession
    ) -> Receipt:
        receipt = await self.repo.get_receipt_by_id_and_user_id(
            object_id=object_id, user_id=user.id, db=db
        )
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found"
            )
        return receipt

    async def get_list_receipts(
        self,
        user: User,
        receipt_filter: ReceiptFilter,
        pagination_params: Params,
        db: AsyncSession,
    ) -> Page[ReceiptReadSchema]:
        paginated_data = await self.repo.get_list_receipts(
            user_id=user.id,
            receipt_filter=receipt_filter,
            pagination_params=pagination_params,
            db=db,
        )

        modified_items = [
            ReceiptReadSchema.model_validate(receipt)
            for receipt in paginated_data.items
        ]
        paginated_data = Page[ReceiptReadSchema](
            items=modified_items,
            total=paginated_data.total,
            page=paginated_data.page,
            size=paginated_data.size,
            pages=paginated_data.pages,
        )
        return paginated_data
