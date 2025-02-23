from typing import Optional
from uuid import UUID

from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.filters.receipt_filters import ReceiptFilter
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

    async def get_by_id(
        self, object_id: UUID | str, db: AsyncSession
    ) -> Optional[Receipt]:
        get_instance_query = (
            select(Receipt)
            .options(selectinload(Receipt.user), selectinload(Receipt.products))
            .filter(Receipt.id == object_id)
        )

        instance = await db.execute(get_instance_query)
        instance = instance.scalar_one_or_none()

        return instance

    async def get_list_receipts(
        self,
        user_id: UUID,
        receipt_filter: ReceiptFilter,
        pagination_params: Params,
        db: AsyncSession,
    ) -> Page[Receipt]:
        get_filtered_list_query = receipt_filter.filter(
            select(Receipt)
            .options(selectinload(Receipt.user), selectinload(Receipt.products))
            .filter(Receipt.user_id == user_id)
        )
        paginated_data = await paginate(
            db, get_filtered_list_query, params=pagination_params
        )

        return paginated_data
