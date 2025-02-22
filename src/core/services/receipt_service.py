from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

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
    ) -> ReceiptReadSchema:
        receipt = await self.repo.get_receipt_by_id_and_user_id(
            object_id=object_id, user_id=user.id, db=db
        )

        receipt_schema = ReceiptReadSchema(
            id=receipt.id,
            products=receipt.products,
            payment=PaymentSchema(type=receipt.payment_type, amount=receipt.amount),
            total=receipt.total,
            rest=receipt.rest,
            created_at=receipt.created_at,
        )
        return receipt_schema

    async def get_list_receipts(
        self, user: User, db: AsyncSession
    ) -> List[ReceiptReadSchema]:
        receipts = await self.repo.get_list_receipts(user_id=user.id, db=db)
        receipt_schemas = [
            ReceiptReadSchema(
                id=receipt.id,
                products=receipt.products,
                payment=PaymentSchema(type=receipt.payment_type, amount=receipt.amount),
                total=receipt.total,
                rest=receipt.rest,
                created_at=receipt.created_at,
            )
            for receipt in receipts
        ]
        return receipt_schemas
