from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.repositories.base_repository import BaseRepository
from src.users.models import User


class UserRepository(BaseRepository):
    model = User

    async def get_by_email(self, email: str, db: AsyncSession):
        get_instance_query = select(User).filter_by(email=email)
        user = await db.execute(get_instance_query)
        user = user.scalar_one_or_none()
        return user
