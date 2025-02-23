from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.repositories.base_repository import BaseRepository, ModelType


class BaseService:
    repo: BaseRepository

    async def get_by_id(self, object_id: UUID | str, db: AsyncSession) -> ModelType:
        retrieved_object = await self.repo.get_by_id(object_id=object_id, db=db)
        if not retrieved_object:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
            )
        return retrieved_object
