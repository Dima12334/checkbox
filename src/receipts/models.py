from sqlalchemy import Column, JSON, ForeignKey, Enum, Numeric
from sqlalchemy.dialects.postgresql import UUID

from src.core.constants import NUMERIC_MAX_DIGITS, NUMERIC_PLACES
from src.core.models import BaseModel
from src.receipts.constants import ReceiptConstants


class Receipt(BaseModel):
    __tablename__ = "receipts"

    products = Column(JSON, nullable=False)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    payment_type = Column(Enum(ReceiptConstants.PaymentTypeEnum), nullable=False)
    amount = Column(Numeric(NUMERIC_MAX_DIGITS, NUMERIC_PLACES), nullable=False)
    rest = Column(Numeric(NUMERIC_MAX_DIGITS, NUMERIC_PLACES), nullable=False)
    total = Column(Numeric(NUMERIC_MAX_DIGITS, NUMERIC_PLACES), nullable=False)
