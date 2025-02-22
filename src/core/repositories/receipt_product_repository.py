from src.core.repositories.base_repository import BaseRepository
from src.receipts.models import ReceiptProduct


class ReceiptProductRepository(BaseRepository):
    model = ReceiptProduct
