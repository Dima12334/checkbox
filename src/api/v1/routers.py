from fastapi import APIRouter

from src.api.v1.auth.routers import auth_router
from src.api.v1.receipts.routers import receipt_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(auth_router, tags=["auth"], prefix="/auth")
api_v1_router.include_router(receipt_router, tags=["receipts"], prefix="/receipts")
