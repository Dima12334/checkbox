from uuid import UUID

from pydantic import BaseModel


class ReadUserSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
