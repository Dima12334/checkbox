from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserReadSchema(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    company_name: str

    model_config = ConfigDict(from_attributes=True)
