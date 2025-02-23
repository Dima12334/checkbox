import textwrap
from decimal import Decimal

from src.receipts.constants import ReceiptConstants
from src.receipts.models import Receipt, ReceiptProduct


class ReceiptTxtGenerator:
    def __init__(
        self,
        receipt: Receipt,
        line_length: int = ReceiptConstants.DEFAULT_TXT_RECEIPT_LINE_LENGTH,
    ):
        self.line_length = line_length

        self.company_name = receipt.user.company_name
        self.products = receipt.products
        self.total = receipt.total
        self.amount = receipt.amount
        self.rest = receipt.rest
        self.receipt_created_at = receipt.created_at.strftime("%d.%m.%Y  %H:%M")

        self.payment_type = receipt.payment_type
        self.payment_type_str = (
            "Готівка"
            if self.payment_type == ReceiptConstants.PaymentTypeEnum.CASH
            else "Картка"
        )

        self.separator = "=" * self.line_length
        self.product_separator = "-" * self.line_length

    def format_product_line(self, product: ReceiptProduct) -> str:
        product_quantity_line = f"{product.quantity} x {product.price:,.2f}"
        product_total = f"{product.total:,.2f}"

        # Combine product name and price for proper wrapping.
        # After wrapping, replace product_total with an empty string
        # and add product_total again, but on the right side.
        product_name_with_price = f"{product.name} {product_total}"

        # Wrap product name to fit within the available width.
        wrapped_name = textwrap.wrap(product_name_with_price, width=self.line_length)
        # Replace product_total with an empty string.
        wrapped_name[-1] = wrapped_name[-1].replace(product_total, "")
        # Add product_total again, but on the right side.
        wrapped_name[-1] = (
            f"{wrapped_name[-1]:<{self.line_length - len(product_total)}}{product_total}"
        )

        return f"{product_quantity_line}\n" + "\n".join(wrapped_name)

    def format_summary_line(self, label: str, amount: Decimal) -> str:
        """Formats a summary line (e.g., total, payment type, rest)."""
        amount_str = f"{amount:,.2f}"
        return f"{label:<{self.line_length - len(amount_str)}}{amount_str}"

    async def generate(self) -> str:
        lines = [
            f"{self.company_name:^{self.line_length}}",
            self.separator,
        ]

        # Add product lines
        for product in self.products:
            lines.append(self.format_product_line(product))
            lines.append(self.product_separator)

        # Replace last product separator with main separator
        lines[-1] = self.separator

        # Add total, payment, and rest details
        lines.extend(
            [
                self.format_summary_line("СУМА", self.total),
                self.format_summary_line(self.payment_type_str, self.amount),
                self.format_summary_line("Решта", self.rest),
                self.separator,
                f"{self.receipt_created_at:^{self.line_length}}",
                f"{'Дякуємо за покупку!':^{self.line_length}}",
            ]
        )

        return "\n".join(lines)
