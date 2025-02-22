from sqlalchemy import Column, JSON, ForeignKey, Enum, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.constants import NUMERIC_MAX_DIGITS, NUMERIC_PLACES
from src.core.models import BaseModel
from src.receipts.constants import ReceiptConstants


class ReceiptProduct(BaseModel):
    __tablename__ = "receipt_product"

    receipt_id = Column(
        UUID(as_uuid=True),
        ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String, nullable=False)
    price = Column(Numeric(NUMERIC_MAX_DIGITS, NUMERIC_PLACES), nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Numeric(NUMERIC_MAX_DIGITS, NUMERIC_PLACES), nullable=False)

    receipt = relationship("Receipt", back_populates="products")


class Receipt(BaseModel):
    __tablename__ = "receipts"

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    payment_type = Column(Enum(ReceiptConstants.PaymentTypeEnum), nullable=False)
    amount = Column(Numeric(NUMERIC_MAX_DIGITS, NUMERIC_PLACES), nullable=False)
    rest = Column(Numeric(NUMERIC_MAX_DIGITS, NUMERIC_PLACES), nullable=False)
    total = Column(Numeric(NUMERIC_MAX_DIGITS, NUMERIC_PLACES), nullable=False)

    products = relationship("ReceiptProduct", back_populates="receipt")
    user = relationship("User", back_populates="receipts")
