from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_async_session
from src.core.dependencies import get_current_user
from src.core.schemas.receipt_schemas import ReceiptReadSchema, ReceiptCreateInSchema
from src.core.services.receipt_service import ReceiptService
from src.users.models import User

receipt_router = APIRouter()


@receipt_router.post("/", response_model=ReceiptReadSchema)
async def create_receipt(
    schema: ReceiptCreateInSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    receipt_servie = ReceiptService()
    return await receipt_servie.create(receipt_info=schema, user=current_user, db=db)


@receipt_router.get("/", response_model=List[ReceiptReadSchema])
async def get_list_receipts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    receipt_servie = ReceiptService()
    return await receipt_servie.get_list_receipts(user=current_user, db=db)


@receipt_router.get("/{receipt_id}", response_model=ReceiptReadSchema)
async def retrieve_receipt(
    receipt_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    receipt_servie = ReceiptService()
    return await receipt_servie.get_receipt_by_id_and_user_id(
        object_id=receipt_id, user=current_user, db=db
    )
