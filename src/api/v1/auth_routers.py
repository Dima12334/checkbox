from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_async_session
from src.core.schemas.auth_schemas import SignUpSchema, SignInSchema, JWTTokenSchema
from src.core.schemas.user_schemas import UserReadSchema
from src.core.services.auth_service import AuthService

auth_router = APIRouter()


@auth_router.post("/sign-up", response_model=UserReadSchema)
async def sign_up(schema: SignUpSchema, db: AsyncSession = Depends(get_async_session)):
    auth_servie = AuthService()
    return await auth_servie.sign_up(user_info=schema, db=db)


@auth_router.post("/sign-in", response_model=JWTTokenSchema)
async def sign_in(schema: SignInSchema, db: AsyncSession = Depends(get_async_session)):
    auth_servie = AuthService()
    return await auth_servie.sign_in(user_info=schema, db=db)
