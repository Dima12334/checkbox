from src.core.repositories.user_repository import UserRepository
from src.core.services.base_service import BaseService


class UserService(BaseService):
    repo = UserRepository()
