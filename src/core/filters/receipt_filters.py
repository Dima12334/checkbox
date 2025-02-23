from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from src.receipts.constants import ReceiptConstants
from src.receipts.models import Receipt


class ReceiptFilter(Filter):
    created_at__gte: Optional[datetime] = None
    created_at__lte: Optional[datetime] = None

    total__gte: Optional[Decimal] = None
    total__lte: Optional[Decimal] = None

    payment_type__in: Optional[list[ReceiptConstants.PaymentTypeEnum]] = None

    class Constants(Filter.Constants):
        model = Receipt
