from enum import Enum


class ReceiptConstants:
    PAYMENT_TYPE_MAX_LENGTH = 8

    MIN_TXT_RECEIPT_LINE_LENGTH = 20
    MAX_TXT_RECEIPT_LINE_LENGTH = 50
    DEFAULT_TXT_RECEIPT_LINE_LENGTH = 25

    class PaymentTypeEnum(str, Enum):
        CASH = "CASH"
        CASHLESS = "CASHLESS"
