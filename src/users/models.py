from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.core.models import BaseModel
from src.users.constants import UserConstants


class User(BaseModel):
    __tablename__ = "users"

    first_name = Column(
        String(length=UserConstants.FIRST_NAME_MAX_LENGTH), nullable=False
    )
    last_name = Column(
        String(length=UserConstants.LAST_NAME_MAX_LENGTH), nullable=False
    )
    company_name = Column(
        String(length=UserConstants.COMPANY_NAME_MAX_LENGTH), nullable=False
    )
    email = Column(
        String(length=UserConstants.EMAIL_MAX_LENGTH), nullable=False, unique=True
    )
    password = Column(String(length=UserConstants.PASSWORD_MAX_LENGTH), nullable=False)

    receipts = relationship("Receipt", back_populates="user")
