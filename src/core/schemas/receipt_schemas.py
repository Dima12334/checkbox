from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field, PositiveInt, ConfigDict, model_validator

from src.core.constants import NUMERIC_MAX_DIGITS, NUMERIC_PLACES
from src.receipts.constants import ReceiptConstants
from src.receipts.models import Receipt


class ReceiptProductCreateInSchema(BaseModel):
    name: str
    price: Decimal = Field(
        max_digits=NUMERIC_MAX_DIGITS, decimal_places=NUMERIC_PLACES, gt=Decimal(0)
    )
    quantity: PositiveInt


class ReceiptProductCreateOutSchema(BaseModel):
    receipt_id: UUID
    name: str
    price: Decimal = Field(
        max_digits=NUMERIC_MAX_DIGITS, decimal_places=NUMERIC_PLACES, gt=Decimal(0)
    )
    quantity: PositiveInt
    total: Decimal = Field(
        max_digits=NUMERIC_MAX_DIGITS, decimal_places=NUMERIC_PLACES, gt=Decimal(0)
    )


class ReceiptProductReadSchema(BaseModel):
    name: str
    price: Decimal
    quantity: PositiveInt
    total: Decimal

    model_config = ConfigDict(from_attributes=True)


class PaymentSchema(BaseModel):
    type: ReceiptConstants.PaymentTypeEnum
    amount: Decimal = Field(
        max_digits=NUMERIC_MAX_DIGITS, decimal_places=NUMERIC_PLACES, gt=Decimal(0)
    )


class ReceiptReadSchema(BaseModel):
    id: UUID
    products: List[ReceiptProductReadSchema]
    payment: PaymentSchema
    total: Decimal
    rest: Decimal
    created_at: datetime

    @model_validator(mode="before")
    def fill_payment(cls, values):
        if isinstance(values, dict):
            if not values.get("payment"):
                values["payment"] = PaymentSchema(
                    type=values.get("payment_type"), amount=values.get("amount")
                )

        if isinstance(values, Receipt):
            if not hasattr(values, "payment"):
                values.payment = PaymentSchema(
                    type=values.payment_type, amount=values.amount
                )

        return values


class ReceiptCreateInSchema(BaseModel):
    products: List[ReceiptProductCreateInSchema]
    payment: PaymentSchema


class ReceiptCreateOutSchema(BaseModel):
    user_id: UUID
    payment_type: ReceiptConstants.PaymentTypeEnum
    amount: Decimal = Field(
        max_digits=NUMERIC_MAX_DIGITS, decimal_places=NUMERIC_PLACES, gt=Decimal(0)
    )
    rest: Decimal = Field(
        max_digits=NUMERIC_MAX_DIGITS, decimal_places=NUMERIC_PLACES, ge=Decimal(0)
    )
    total: Decimal = Field(
        max_digits=NUMERIC_MAX_DIGITS, decimal_places=NUMERIC_PLACES, gt=Decimal(0)
    )
