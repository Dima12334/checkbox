from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.base_repository import BaseRepository, ModelType


class BaseService:
    repo: BaseRepository

    async def get_by_id(self, object_id: UUID | str, db: AsyncSession) -> ModelType:
        return await self.repo.get_by_id(object_id=object_id, db=db)
