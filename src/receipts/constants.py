from enum import Enum


class ReceiptConstants:
    PAYMENT_TYPE_MAX_LENGTH = 8

    class PaymentTypeEnum(str, Enum):
        CASH = "CASH"
        CASHLESS = "CASHLESS"
