from uuid import UUID

from pydantic import BaseModel


class UserReadSchema(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    company_name: str

    class Config:
        orm_mode = True
