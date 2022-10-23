from typing import List
from fastapi.responses import JSONResponse
from fastapi import status
from src.models.db import User


class UserService:
    @staticmethod
    def get_users() -> List[User]:
        return User.objects.all()

    @staticmethod
    async def create_user(user: User) -> JSONResponse:
        print("Creating new user...")
        user_in_db = await User.objects.filter(username=user.username).get_or_none()

        if user_in_db is None:
            await user.save()
            return JSONResponse(
                content=f"Username {user.username} registered successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        return JSONResponse(
            content=f"Username {user.username} already registered.",
            status_code=status.HTTP_409_CONFLICT,
        )
