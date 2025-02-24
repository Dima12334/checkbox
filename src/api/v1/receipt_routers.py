from uuid import UUID
from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from fastapi_pagination import Params, Page
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response
from config.database import get_async_session
from src.core.dependencies import get_current_user
from src.core.filters.receipt_filters import ReceiptFilter
from src.core.schemas.receipt_schemas import ReceiptReadSchema, ReceiptCreateInSchema
from src.core.services.receipt_service import ReceiptService
from src.receipts.constants import ReceiptConstants
from src.users.models import User

receipt_router = APIRouter()


@receipt_router.post(
    "/", response_model=ReceiptReadSchema, status_code=status.HTTP_201_CREATED
)
async def create_receipt(
    schema: ReceiptCreateInSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    **Authorization**: Requires `Bearer <JWT Token>` in the `Authorization` header.
    """
    receipt_servie = ReceiptService()
    return await receipt_servie.create(receipt_info=schema, user=current_user, db=db)


@receipt_router.get("/", response_model=Page[ReceiptReadSchema])
async def get_list_receipts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    receipt_filter: ReceiptFilter = FilterDepends(ReceiptFilter),
    pagination_params: Params = Depends(),
):
    """
    **Authorization**: Requires `Bearer <JWT Token>` in the `Authorization` header.
    """
    receipt_servie = ReceiptService()
    return await receipt_servie.get_list_receipts(
        user=current_user,
        receipt_filter=receipt_filter,
        pagination_params=pagination_params,
        db=db,
    )


@receipt_router.get("/{receipt_id}", response_model=ReceiptReadSchema)
async def retrieve_receipt(
    receipt_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    **Authorization**: Requires `Bearer <JWT Token>` in the `Authorization` header.
    """
    receipt_servie = ReceiptService()
    return await receipt_servie.get_receipt_by_id_and_user_id(
        object_id=receipt_id, user=current_user, db=db
    )


@receipt_router.get("/{receipt_id}/print", response_class=Response)
async def print_receipt(
    receipt_id: UUID,
    line_length: int = Query(
        ge=ReceiptConstants.MIN_TXT_RECEIPT_LINE_LENGTH,
        le=ReceiptConstants.MAX_TXT_RECEIPT_LINE_LENGTH,
        default=ReceiptConstants.DEFAULT_TXT_RECEIPT_LINE_LENGTH,
    ),
    db: AsyncSession = Depends(get_async_session),
) -> Response:
    """
    **Authorization**: Not required.
    """
    receipt_servie = ReceiptService()
    receipt_txt = await receipt_servie.print_receipt(
        object_id=receipt_id, line_length=line_length, db=db
    )

    return Response(content=receipt_txt, media_type="text/plain")
