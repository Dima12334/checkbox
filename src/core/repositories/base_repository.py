from typing import TypeVar
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.models import BaseModel as DBBaseModel


ModelType = TypeVar("ModelType", bound=DBBaseModel)
PydanticModelType = TypeVar("PydanticModelType", bound=BaseModel)


class BaseRepository:
    model: ModelType

    async def create(self, schema: PydanticModelType, db: AsyncSession):
        new_object = self.model(**schema.dict())

        db.add(new_object)
        await db.commit()
        await db.refresh(new_object)

        return new_object

    async def get_by_id(self, object_id: UUID, db: AsyncSession):
        get_instance_query = select(self.model).filter(self.model.id == object_id)
        instance = await db.execute(get_instance_query)
        instance = instance.scalar_one_or_none()

        return instance
