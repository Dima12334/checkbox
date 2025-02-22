from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.repositories.base_repository import BaseRepository
from src.receipts.models import Receipt


class ReceiptRepository(BaseRepository):
    model = Receipt

    async def get_receipt_by_id_and_user_id(
        self, object_id: UUID | str, user_id: UUID, db: AsyncSession
    ) -> Optional[Receipt]:
        get_instance_query = (
            select(Receipt)
            .options(selectinload(Receipt.user), selectinload(Receipt.products))
            .filter(Receipt.id == object_id, Receipt.user_id == user_id)
        )

        instance = await db.execute(get_instance_query)
        instance = instance.scalar_one_or_none()

        return instance

    async def get_list_receipts(self, user_id: UUID, db: AsyncSession):
        get_list_query = (
            select(Receipt)
            .options(selectinload(Receipt.user), selectinload(Receipt.products))
            .filter(Receipt.user_id == user_id)
        )

        instances = await db.execute(get_list_query)
        instances = instances.scalars().all()

        return instances
