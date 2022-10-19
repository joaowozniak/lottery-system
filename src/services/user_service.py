from typing import List
from src.models.db import User


class UserService:
    @staticmethod
    def get_users() -> List[User]:
        return User.objects.all()

    @staticmethod
    async def create_user(user: User):
        return await user.save()
