from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import (
    InvalidUsernameOrPasswordException,
    ObjectAlreadyExistsException,
)
from src.core.repositories.user_repository import UserRepository
from src.core.schemas.auth_schemas import SignUpSchema, SignInSchema, JWTTokenSchema
from src.core.services.base_service import BaseService
from src.core.utils.jwt import create_jwt
from src.core.utils.password import get_password_hash, verify_password


class AuthService(BaseService):
    repo = UserRepository()

    async def sign_in(self, user_info: SignInSchema, db: AsyncSession):
        user = await self.repo.get_by_email(user_info.email, db)
        if not user:
            raise InvalidUsernameOrPasswordException()
        if not await verify_password(
            plain_password=user_info.password, hashed_password=user.password
        ):
            raise InvalidUsernameOrPasswordException()

        access_token = await create_jwt(user=user)
        return JWTTokenSchema(access_token=access_token)

    async def sign_up(self, user_info: SignUpSchema, db: AsyncSession):
        existed_user = await self.repo.get_by_email(user_info.email, db)
        if existed_user:
            raise ObjectAlreadyExistsException()

        user_info.password = await get_password_hash(user_info.password)
        created_user = await self.repo.create(user_info, db)
        return created_user
