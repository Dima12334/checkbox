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

    async def create_bulk(self, schemas: list[PydanticModelType], db: AsyncSession):
        new_objects = [self.model(**schema.dict()) for schema in schemas]

        db.add_all(new_objects)
        await db.commit()

        new_objects_ids = [obj.id for obj in new_objects]
        refreshed_new_objects_query = select(self.model).where(
            self.model.id.in_(new_objects_ids)
        )
        refreshed_new_objects = await db.execute(refreshed_new_objects_query)
        refreshed_new_objects = refreshed_new_objects.scalars().all()

        return refreshed_new_objects

    async def get_by_id(self, object_id: UUID | str, db: AsyncSession):
        get_instance_query = select(self.model).filter(self.model.id == object_id)
        instance = await db.execute(get_instance_query)
        instance = instance.scalar_one_or_none()

        return instance
