from datetime import datetime
from pydantic import BaseModel, Field
from src.users.constants import UserConstants


class JWTTokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class JWTTokenPayloadSchema(BaseModel):
    id: str
    exp: datetime | int


class SignInSchema(BaseModel):
    email: str = Field(max_length=UserConstants.EMAIL_MAX_LENGTH)
    password: str = Field(max_length=UserConstants.PASSWORD_MAX_LENGTH)


class SignUpSchema(BaseModel):
    email: str = Field(max_length=UserConstants.EMAIL_MAX_LENGTH)
    password: str = Field(max_length=UserConstants.PASSWORD_MAX_LENGTH)
    first_name: str = Field(max_length=UserConstants.FIRST_NAME_MAX_LENGTH)
    last_name: str = Field(max_length=UserConstants.LAST_NAME_MAX_LENGTH)
