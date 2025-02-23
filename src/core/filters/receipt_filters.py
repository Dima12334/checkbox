from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from src.receipts.constants import ReceiptConstants
from src.receipts.models import Receipt


class ReceiptFilter(Filter):
    created_at__gte: Optional[datetime] = Field(None, alias="created_at_from")
    created_at__lte: Optional[datetime] = Field(None, alias="created_at_to")

    total__gte: Optional[Decimal] = Field(None, alias="total_from")
    total__lte: Optional[Decimal] = Field(None, alias="total_to")

    payment_type__in: Optional[list[ReceiptConstants.PaymentTypeEnum]] = Field(
        None, alias="payment_types"
    )

    class Constants(Filter.Constants):
        model = Receipt

    class Config:
        populate_by_name = True
