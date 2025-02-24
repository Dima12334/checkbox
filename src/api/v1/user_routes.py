from fastapi import APIRouter, Depends

from src.core.dependencies import get_current_user
from src.core.schemas.user_schemas import UserReadSchema
from src.users.models import User

user_router = APIRouter()


@user_router.get("/me", response_model=UserReadSchema)
async def get(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current user.

    **Authorization**: Requires `Bearer <JWT Token>` in the `Authorization` header.
    """
    return current_user
